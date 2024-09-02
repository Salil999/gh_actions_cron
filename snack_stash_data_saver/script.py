import os
import boto3
import requests
import datetime
import time

access_key = os.environ.get('BUSINESS_AWS_ACCESS_KEY')
secret_key = os.environ.get('BUSINESS_AWS_SECRET_KEY')
table_name = os.environ.get('BUSINESS_DYNAMODB_TABLE_NAME')
zero_sheets_api_key = os.environ.get('BUSINESS_ZEROSHEETS_API_KEY')

# Create a session using the access keys and secret keys
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='us-east-1'
)

# Create a DynamoDB client using the session
dynamodb = session.client('dynamodb')

google_sheets_content = requests.get(
    "https://api.zerosheets.com/v1/zwb",
    headers={
        "Authorization": "Bearer " + zero_sheets_api_key,
    },
)
google_sheets_data = google_sheets_content.json()

for item in google_sheets_data:
    for item in google_sheets_data:
        # Expire time is set to 3 years from the current date
        current_time = int(time.time())
        current_date_time = datetime.datetime.fromtimestamp(current_time)
        expire_time = current_date_time + datetime.timedelta(days = (365 * 3))
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'product_name': {'S': item.get('Product Name', '')},
                'original_quantity': {'S': item.get('Original Quantity', '')},
                'amount_put_into_machine': {'S': item.get('Amount Put Into Machine', '')},
                'left_over': {'S': item.get('Left Over', '')},
                'amount_thrown': {'S': item.get('Amount Thrown', '')},
                'insert_time': {'N': str(current_time)},
                'expireAt': {'N': str(expire_time.timestamp())}
            }
        )
        # Sleep for 0.5 seconds to avoid throttling
        time.sleep(0.5)
