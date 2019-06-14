import os
import json

from user import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch user from the database
    result = table.get_item(
        Key={
            'username': event['pathParameters']['username']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
