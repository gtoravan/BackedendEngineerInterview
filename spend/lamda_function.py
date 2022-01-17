import json
import boto3
from datetime import datetime

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    data = client.scan(
        TableName='points_database'
    )
    items = data["Items"]

    spend_points = (event["body"])
    spend_points = json.loads(spend_points)
    spend_points = int(spend_points["points"])

    transaction_dict = []

    for i in items:
        temp_list = {}
        temp_list["ID"] = i["ID"]["S"]
        temp_list["payer"] = i["payer"]["S"]
        temp_list["points"] = int(i["points"]["S"])
        timestamp_str = i["timestamp"]["S"]
        d = datetime.fromisoformat(timestamp_str)
        d = d.strftime('%Y-%m-%d %H:%M:%S')
        temp_list["timestamp"] = d
        transaction_dict.append(temp_list)

    transaction_dict = (sorted(transaction_dict, key=lambda x: x["timestamp"]))

    expenditure = {}

    for transac in transaction_dict:
        if transac["payer"] not in expenditure:
            expenditure[transac["payer"]] = 0
        if transac["points"] < spend_points:
            expenditure[transac["payer"]] = expenditure[transac["payer"]] + transac["points"]
            spend_points -= transac["points"]
            transac["points"] = 0
        elif transac["points"] == spend_points:
            expenditure[transac["payer"]] = expenditure[transac["payer"]] + transac["points"]
            transac["points"] = 0
            spend_points = 0
            break
        elif transac["points"] > spend_points:
            transac["points"] = transac["points"] - spend_points
            expenditure[transac["payer"]] = expenditure[transac["payer"]] + spend_points
            spend_points = 0
            break

    for new in transaction_dict:
        update = client.update_item(TableName='points_database', Key={'ID': {"S": new["ID"]}},
                                    UpdateExpression='SET points = :p',
                                    ExpressionAttributeValues={":p": {"S": str(new["points"])}},
                                    ReturnValues="UPDATED_NEW")

    ret_list = []

    for k, v in expenditure.items():
        ret_list.append({"payer": k, "points": -v})

    response = {
        'statusCode': 200,
        'body': json.dumps(ret_list),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

    return response


