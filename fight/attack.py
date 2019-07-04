import os
import json
import time

from fight import enemies
from ffconfig import items
import boto3
from random import randint
dynamodb = boto3.resource('dynamodb')


def attack(event, context):
    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    # fetch user from the database
    username = event['headers']['username']
    user_row = table.get_item( Key={ 'username': username } )['Item']
    
    if user_row['active_fight'] == "No active fight":
        # user already fighting
        # create a response
        response = {
            "statusCode": 200,
            "body": "Not in a fight"
        }
    else:
        enemy = json.loads(user_row['active_fight'])
        user_weapon = items.weapons_dict[int(user_row['weapon'])]
        timestamp = int(time.time() * 1000)
        # user hits the enemy
        new_enemy_health = int(enemy['health']) - int(user_weapon['damage'])
        enemy['health'] = new_enemy_health
        if new_enemy_health <= 0:
            # user won the fight
            result = table.update_item(
                Key={
                    'username': username
                },
                ExpressionAttributeValues={
                  ':active_fight': 'No active fight',
                  ':last_fight': json.dumps(enemy),
                  ':xp': int(user_row['xp']) + int(enemy['xp']),
                  ':money': int(user_row['money']) + int(enemy['money']),
                  ':enemy_fights_remaining': int(user_row['enemy_fights_remaining']) - 1,
                  ':updatedAt': timestamp,
                },
                UpdateExpression='SET active_fight = :active_fight, '
                                 'last_fight = :last_fight, '
                                 'xp = :xp, '
                                 'money = :money, '
                                 'enemy_fights_remaining = :enemy_fights_remaining, '
                                 'updatedAt = :updatedAt',
                ReturnValues='ALL_NEW',
            )
            # create a response
            response = {
                "statusCode": 200,
                "body": "You beat "+enemy['name']+"!"
            }
        else:
            # user gets hit
            new_user_health = int(user_row['health']) - int(enemy['damage'])
            # TODO: check if the user died here and do something
            result = table.update_item(
                Key={
                    'username': username
                },
                ExpressionAttributeValues={
                  ':health': new_user_health,
                  ':active_fight': json.dumps(enemy),
                  ':updatedAt': timestamp,
                },
                UpdateExpression='SET health = :health, '
                                 'active_fight = :active_fight, '
                                 'updatedAt = :updatedAt',
                ReturnValues='ALL_NEW',
            )
            # create a response
            response = {
                "statusCode": 200,
                "body": "You hit "+enemy['name']+", but they hit you right back!"
            }
        
        
    return response