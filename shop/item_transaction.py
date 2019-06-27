import os
import json
import time

from user import decimalencoder
import boto3

def item_transaction(table, username, field, field_value, money):
    colonfield = ':'+field
    timestamp = int(time.time() * 1000)
    result = table.update_item(
        Key={
            'username': username
        },
        ExpressionAttributeValues={
          colonfield: field_value,
          ':money': money,
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET '+field+' = '+colonfield+', '
                         'money = :money, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )
    
    # remove the password field, it causes problems
    result['Attributes'].pop('password', None)

    return result