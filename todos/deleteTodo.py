import json
import os
import logging
import jwt
import uuid
import base64
import boto3
from botocore.exceptions import ClientError
dynamodb = boto3.resource('dynamodb')

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    auth = jwt.decode(event['headers']["authorization"],
                      options={"verify_signature": False})
    userId = auth['sub']

    if (not userId):
        return {
            'statusCode': 400,
            'body': "invalid request, you are missing the parameter body"
        }

    try:
        response = table.delete_item(
            Key={
                'userId': userId,
                'todoId': event['pathParameters']['id']
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response
