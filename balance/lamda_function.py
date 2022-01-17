import json
import boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    data = client.scan(
        TableName='points_database'
    )
    items = data["Items"]
    return_dict = {}
    for i in items:
        if i["payer"]["S"] not in return_dict:
            return_dict[i["payer"]["S"]] = int(i["points"]["S"])
        else:
            return_dict[i["payer"]["S"]] += int(i["points"]["S"])
    response = {
        'statusCode': 200,
        'body': json.dumps(return_dict),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

    return response

