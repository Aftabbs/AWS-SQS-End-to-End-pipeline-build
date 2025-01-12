import os
import boto3
import json
import redis
from shared.utils import get_redis_connection, ensure_queue_exists, clean_message, validate_message, extract_essential_fields

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localstack:4566")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

sqs = boto3.client('sqs', endpoint_url=AWS_ENDPOINT, region_name='us-east-1')
redis_client = get_redis_connection(REDIS_HOST, REDIS_PORT)

queue_url = ensure_queue_exists(sqs, "OrderQueue")

def update_redis(data):
    user_key = f"user:{data['user_id']}"
    global_key = "global:stats"

    # Update user stats
    redis_client.hincrby(user_key, "order_count", 1)
    redis_client.hincrbyfloat(user_key, "total_spend", data['order_value'])

    # Update global stats
    redis_client.hincrby(global_key, "total_orders", 1)
    redis_client.hincrbyfloat(global_key, "total_revenue", data['order_value'])


def process_message(message):
    try:
        body = json.loads(message['Body'])
        print(f"Processing message: {body}")
        
        body = clean_message(body)
        print(f"Cleaned message: {body}")
        
        is_valid, validation_msg = validate_message(body)

        if is_valid:
            essential_data = extract_essential_fields(body)
            print(f"Extracted data: {essential_data}")
                
                
            update_redis(essential_data)
            print("Message processed successfully.")
        else:
            print(f"Invalid message: {validation_msg}")

        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

    except json.JSONDecodeError as e:
        print(f"Error parsing message: {e}")
        print(f"Raw Message: {message['Body']}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def poll_messages():
    """Poll SQS for messages and process them."""
    while True:
        print("Polling for messages...")
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)
        messages = response.get('Messages', [])
        
        if not messages:
            print("No messages found.")
        for message in messages:
            process_message(message)

if __name__ == "__main__":
    poll_messages()
