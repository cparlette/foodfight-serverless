import os
import json
import time

from user import decimalencoder
from shop import item_transaction
from ffconfig import items
import boto3
dynamodb = boto3.resource('dynamodb')


def sell_armor(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch user from the database
    username = event['headers']['username']
    user_row = table.get_item( Key={ 'username': username } )['Item']
    armor_id = int(user_row['armor'])
    armor_to_sell = items.armor_dict[armor_id]
    user_money = int(user_row['money'])
    sale_value = armor_to_sell['cost'] * .5
    user_money += int(sale_value)
    # update the user in the database
    result = item_transaction.item_transaction(table, username, 'armor', 1, user_money)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }
    return response