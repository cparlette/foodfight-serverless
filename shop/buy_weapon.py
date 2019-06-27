import os
import json
import time

from user import decimalencoder
from shop import item_transaction
from ffconfig import items
import boto3
dynamodb = boto3.resource('dynamodb')


def buy_weapon(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch user from the database
    username = event['headers']['username']
    user_row = table.get_item( Key={ 'username': username } )['Item']
    weapon_id = int(event['pathParameters']['weapon_id'])
    weapon_to_buy = items.weapons_dict[weapon_id]
    user_money = int(user_row['money'])
    if user_money < weapon_to_buy['cost']:
        # user can't afford the weapon
        # create a response
        response = {
            "statusCode": 200,
            "body": "Insufficient Funds"
        }
    else:
        user_money -= weapon_to_buy['cost']
        # update the user in the database
        result = item_transaction.item_transaction(table, username, 'weapon', weapon_id, user_money)

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'],
                               cls=decimalencoder.DecimalEncoder)
        }
    return response