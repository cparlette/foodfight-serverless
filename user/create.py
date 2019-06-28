import json
import logging
import os
import time
import uuid
import base64

import boto3
dynamodb = boto3.resource('dynamodb')


def encrypt_password_to_b64(key_id=None, password=None):
    kms_client = boto3.client('kms')
    encrypted = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=password
    )
    encrypted_b64 = base64.b64encode(encrypted['CiphertextBlob'])
    return encrypted_b64

def create(event, context):
    data = json.loads(event['body'])
    if 'username' not in data:
        logging.error("Validation Failed - no username provided")
        raise Exception("Couldn't create the user - no username provided")
    if 'password' not in data:
        logging.error("Validation Failed - no password provided")
        raise Exception("Couldn't create the user - no password provided")

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['USER_DYNAMODB_TABLE'])

    encrypted_password = encrypt_password_to_b64(os.environ['KMS_KEY_ID'], data['password'])

    item = {
        'username': data['username'],
        'password': encrypted_password,
        'createdAt': timestamp,
        'updatedAt': timestamp,
        'weapon': 1,
        'armor': 1,
        'money': 500,
        'health': 100,
        'STR': 10,
        'DEX': 10,
        'POT': 10,
        'CON': 10,
        'MYS': 10,
        'INT': 10,
        'level': 1,
        'xp': 0,
        'wins': 0,
        'losses': 0,
        'user_fights_remaining': 5,
        'enemy_fights_remaining': 10,
    }

    # write the user to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({'username': data['username'], 'createdAt': timestamp})
    }

    return response
