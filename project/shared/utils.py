import redis

def get_redis_connection(host, port):
    return redis.Redis(host=host, port=port, decode_responses=True)

def ensure_queue_exists(sqs, queue_name):
    response = sqs.create_queue(QueueName=queue_name)
    return response['QueueUrl']

def clean_message(body):
    """Clean the structure and values of the order message."""
    # Trim and normalize fields
    body['order_id'] = body['order_id'].strip().upper()
    body['user_id'] = body['user_id'].strip().upper()
    body['payment_method'] = body['payment_method'].strip().upper()

    body['shipping_address'] = body['shipping_address'].strip()

    for item in body['items']:
        item['product_id'] = item['product_id'].strip().upper()
        item['quantity'] = int(item['quantity'])  
        item['price_per_unit'] = float(item['price_per_unit'])  

    return body

def validate_message(body):
    """Validate the structure and values of the order message."""
    required_fields = ['order_id', 'user_id', 'order_value', 'items']
    if not all(field in body for field in required_fields):
        return False, "Missing required fields."

    calculated_value = sum(item['quantity'] * item['price_per_unit'] for item in body['items'])
    if not (round(calculated_value, 2) == round(body['order_value'], 2)):
        return False, f"Order value mismatch. Expected {round(calculated_value, 2)}, got {body['order_value']}."

    return True, "Valid"

def extract_essential_fields(body):
    """Extract essential fields for aggregation."""
    return {
        "user_id": body["user_id"],
        "order_value": body["order_value"],
        "order_timestamp": body["order_timestamp"]
    }
