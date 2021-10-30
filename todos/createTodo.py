import json
import os
import logging
import jwt
import uuid
import base64
import boto3

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
# Get the service resource.
dynamodb = boto3.resource('dynamodb')


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))
    # Pull out the DynamoDB table name from environment
    table_name = os.environ.get('DYNAMODB_TABLE')

    if (not event['body']):
        return {
            'statusCode': 400,
            'body': "invalid request, you are missing the parameter body"
        }
    s = base64.b64decode(event['body'])
    print(s)
    print(s.decode())
    item = json.loads(s.decode())
    auth = jwt.decode(event['headers']["authorization"],
                      options={"verify_signature": False})

    LOG.debug("auth::::: " + json.dumps(auth))
    item["userId"] = auth['sub']
    item["todoId"] = str(uuid.uuid4())
    item["test"] = "aaaa"

    LOG.debug("finish " + json.dumps(item["todoId"]))
    # Get my table
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(
            Item=item)
        LOG.debug("RESPONSE: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {'statusCode': 500,
                'body': str(e)
                }


# import json
# import logging
# import os
# import time
# import uuid

# import boto3
# dynamodb = boto3.resource('dynamodb')


# def create(event, context):
#     data = json.loads(event['body'])
#     if 'text' not in data:
#         logging.error("Validation Failed")
#         raise Exception("Couldn't create the todo item.")
    
#     timestamp = str(time.time())

#     table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

#     item = {
#         'id': str(uuid.uuid1()),
#         'text': data['text'],
#         'checked': False,
#         'createdAt': timestamp,
#         'updatedAt': timestamp,
#     }

#     # write the todo to the database
#     table.put_item(Item=item)

#     # create a response
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(item)
#     }

#     return response