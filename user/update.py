import json
import time
import logging
import os

from user import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'weapon' not in data or 'armor' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the user.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # update the user in the database
    result = table.update_item(
        Key={
            'username': event['pathParameters']['username']
        },
        ExpressionAttributeValues={
          ':weapon': data['weapon'],
          ':armor': data['armor'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET weapon = :weapon, '
                         'armor = :armor, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # remove the password field, it causes problems
    result['Attributes'].pop('password', None)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
