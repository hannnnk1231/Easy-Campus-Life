import json
import boto3
import random
import requests
from requests_aws4auth import AWS4Auth
from boto3.dynamodb.conditions import Attr

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def searchES(username):
    response = requests.post(HOST+"events/_search?size=10000", auth=awsauth, headers={"Content-Type":"application/json"})
    events = sorted([{**event["_source"], **{"id":event["_id"]}} for event in json.loads(response.text)['hits']['hits']], key = lambda e:e['time'])
    return {"recommend": events[random.randint(0, len(events)-1)], "all": events}

def lambda_handler(event, context):
    # TODO implement
    username = event['queryStringParameters']['username']

    res = searchES(username)
    return {
        'statusCode': 200,
        'body': json.dumps(res),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
