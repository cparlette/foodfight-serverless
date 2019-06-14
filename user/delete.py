import os

import boto3
dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # delete the user from the database
    table.delete_item(
        Key={
            'id': event['pathParameters']['username']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
