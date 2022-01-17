import json
import boto3
from datetime import datetime

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    transaction = event["body"]
    transaction = json.loads(transaction)

    timestamp_str = transaction["timestamp"]
    d = datetime.fromisoformat(timestamp_str[:-1])
    d = d.strftime('%Y-%m-%d %H:%M:%S')

    transaction["timestamp"] = d

    data = client.put_item(
        TableName='points_database',
        Item={
            'ID': {
                'S': transaction["payer"] + "|" + str(transaction["points"]) + "|" + transaction["timestamp"]
            },
            'payer': {
                'S': transaction["payer"]
            },
            'points': {
                'S': str(transaction["points"])
            },
            'timestamp': {
                'S': str(transaction["timestamp"])
            }
        }
    )

    response = {
        'statusCode': 200,
        'body': "Transaction Added",
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

    return response