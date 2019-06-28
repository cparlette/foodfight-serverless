import os
import json
import time

from user import decimalencoder
from shop import item_transaction
from ffconfig import items
import boto3
dynamodb = boto3.resource('dynamodb')


def buy_armor(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch user from the database
    username = event['headers']['username']
    user_row = table.get_item( Key={ 'username': username } )['Item']
    armor_id = int(event['pathParameters']['armor_id'])
    armor_to_buy = items.armor_dict[armor_id]
    user_money = int(user_row['money'])
    if user_money < armor_to_buy['cost']:
        # user can't afford the armor
        # create a response
        response = {
            "statusCode": 200,
            "body": "Insufficient Funds"
        }
    else:
        user_money -= armor_to_buy['cost']
        # update the user in the database
        result = item_transaction.item_transaction(table, username, 'armor', armor_id, user_money)

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'],
                               cls=decimalencoder.DecimalEncoder)
        }
    return response