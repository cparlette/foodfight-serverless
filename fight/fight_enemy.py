import os
import json
import time

from user import decimalencoder
from shop import item_transaction
from fight import enemies
import boto3
from random import randint
dynamodb = boto3.resource('dynamodb')


def fight_enemy(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch user from the database
    username = event['headers']['username']
    user_row = table.get_item( Key={ 'username': username } )['Item']
    
    if user_row['active_fight'] != "No active fight":
        # user already fighting
        # create a response
        response = {
            "statusCode": 200,
            "body": "Already in a fight"
        }
    else:
        enemy_level = int(event['pathParameters']['enemy_level'])
        random_enemy_int = randint(1,8)
        enemy = enemies.enemies[enemy_level][random_enemy_int]
        # update the user in the database
        timestamp = int(time.time() * 1000)
        result = table.update_item(
            Key={
                'username': username
            },
            ExpressionAttributeValues={
              ':active_fight': json.dumps(enemy),
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET active_fight = :active_fight, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )
        # create a response
        response = {
            "statusCode": 200,
            "body": "Your fight with "+enemy['name']+" has begun!"
        }
    return response