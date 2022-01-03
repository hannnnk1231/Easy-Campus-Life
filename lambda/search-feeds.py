import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
from boto3.dynamodb.conditions import Attr

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


def pull_info(username):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Profile-zvvjx5wqajabjkac7tm6ise3qu-dev')
    try:
        response = table.scan(FilterExpression=Attr('id').eq(username))
        info = response["Items"][0]
    except IndexError:
        logger.debug("Error pull username {} info from dynamodb".format(username))
        return
    return info['displayName']


def searchES(w_id, channel):
    response = requests.post(HOST+"feeds/_search?q=w_id:{}&size=10000".format(w_id), auth=awsauth, headers={"Content-Type":"application/json"})
    feeds = sorted([feed["_source"] for feed in json.loads(response.text)['hits']['hits'] if feed["_source"]['channel']==channel], key = lambda f:f['time'])
    for feed in feeds:
      feed['profilename'] = pull_info(feed['username'])
      feed['profileimg'] = "https://easycampusreactv20f8fa0a551e84b23b27048be4f0649145029-dev.s3.amazonaws.com/public/{}.jpg".format(feed['username'])
    return feeds

def searchES_users(w_id):
    response = requests.post(HOST+"workspace_user/_search?q=w_id:{}&size=10000".format(w_id), auth=awsauth, headers={"Content-Type":"application/json"})
    print(response)
    users = [{"username": w["_source"]['username']} for w in json.loads(response.text)['hits']['hits']]
    for user in users:
      user['profilename'] = pull_info(user["username"])
      user['profileimg'] = "https://easycampusreactv20f8fa0a551e84b23b27048be4f0649145029-dev.s3.amazonaws.com/public/{}.jpg".format(user['username'])
    return users

def lambda_handler(event, context):
    # TODO implement
    w_id, channel = event['queryStringParameters']['w_id'], event['queryStringParameters']['channel']

    res = {
      "feeds": searchES(w_id, channel),
      "users": searchES_users(w_id)
    }
    print(res)
    return {
        'statusCode': 200,
        'body': json.dumps(res),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
