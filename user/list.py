import json
import os

from user import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def list(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch all users from the database
    result = table.scan()

    for item in result['Items']:
    	item.pop('password', None)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
