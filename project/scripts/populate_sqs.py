import boto3
import pandas as pd
import json

sqs = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",  
    region_name="us-east-1",
    aws_access_key_id="fake_access_key",  # Dummy credentials for LocalStack
    aws_secret_access_key="fake_secret_key"
)

queue_url = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/OrderQueue"

excel_file = "project\scripts\orders.xlsx"  # Replace with the relative path of the source file
data = pd.read_excel(excel_file)

for index, row in data.iterrows():
    message = {
        "order_id": row["order_id"],
        "user_id": row["user_id"],
        "order_timestamp": row["order_timestamp"],
        "order_value": row["order_value"],
        "items": json.loads(row["items"]),  
        "shipping_address": row["shipping_address"],
        "payment_method": row["payment_method"]
    }
    # Send the message to SQS
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
    print(f"Message sent for order_id={row['order_id']}: {response}")
