import base64
import boto3
import os
import json


def basicAuth(event, context):
    username = None
    password = None

    # Look in the headers for username and password
    # TODO: there's lots in event here, might want to check other fields for user/pass
    if 'username' in event['headers']:
        username = event['headers']['username']
    else:
        print("Headers missing username")
        raise Exception("Unauthorized due to missing username headers")
    if 'password' in event['headers']:
        password = event['headers']['password']
    else:
        print("Headers missing password")
        raise Exception("Unauthorized due to missing password headers")

    # get the user info from DynamoDB
    # TODO: there's a lot of assumptions here, handle errors better
    table = boto3.resource('dynamodb').Table(os.environ['USER_DYNAMODB_TABLE'])
    user_row = table.get_item( Key = { 'username': username } )
    encrypted_password = user_row['Item']['password'].value
    decrypted_password = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(encrypted_password))['Plaintext'].decode()
    if decrypted_password == password:
        # successful authentication
        authResponse = {
            "principalId": username,
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {"Action": "execute-api:Invoke", "Effect": "Allow", "Resource": event['methodArn']}
                ],
            },
            "context": {"username": username}
        }
        print("Authentication response: %s" % authResponse)
        return authResponse
    else:
        print("Wrong password provided for user "+username)
        raise Exception("Unauthorized due to wrong password for user "+username)
