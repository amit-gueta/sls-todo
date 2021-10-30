import json
import os
import logging
import jwt
import uuid
import base64
import boto3
from boto3.dynamodb.conditions import Key

from todos import decimalencoder

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))
    # Pull out the DynamoDB table name from environment
    table_name = os.environ.get('DYNAMODB_TABLE')

    auth = jwt.decode(event['headers']["authorization"],
                      options={"verify_signature": False})

    userId = auth['sub']
    if (not userId):
        return {
            'statusCode': 400,
            'body': "invalid request, you are missing the parameter body"
        }

    s = base64.b64decode(event['body'])
    item = json.loads(s.decode())

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # Get my table
    table = dynamodb.Table(table_name)
    LOG.debug("RESPONSE: " + json.dumps(userId))
    try:
        response = table.update_item(
            Key={
                'userId': userId,
                'todoId': event['pathParameters']["id"]
            },
            UpdateExpression="set title=:t, content=:c",
            ExpressionAttributeValues={
                ':t': item['title'],
                ':c': item['content']
            },
            ReturnValues="UPDATED_NEW"
        )
        LOG.info("RESPONSE: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps(response['ResponseMetadata']['HTTPStatusCode'], indent=4, cls=decimalencoder.DecimalEncoder)
        }
    except Exception as e:
        return {'statusCode': 500,
                'body': str(e)
                }
