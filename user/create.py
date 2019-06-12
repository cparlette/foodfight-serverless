import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'username' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the user.")

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'username': data['username'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the user to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
