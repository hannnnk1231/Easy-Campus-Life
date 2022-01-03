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
        info = response["Items"]
        while('LastEvaluatedKey' in response):
            LastEvaluatedKey = response['LastEvaluatedKey']
            response = table.scan(FilterExpression=Attr('id').eq(username), ExclusiveStartKey=LastEvaluatedKey)
            info += response["Items"]
        info = info[0]
    except IndexError:
        logger.debug("Error pull user {} info from dynamodb".format(username))
        return
    return info

def searchES(username):
    response = requests.post(HOST+"workspace_user/_search?q=username:{}&size=10000".format(username), auth=awsauth,headers={"Content-Type":"application/json"})
    return sorted([w["_source"] for w in json.loads(response.text)['hits']['hits']], key = lambda f:f['workspaceName'], reverse=True)

def lambda_handler(event, context):
    # TODO implement
    username = event['queryStringParameters']['username']
    if event['queryStringParameters']['event'] == 'ws':
        res = searchES(username)
    elif event['queryStringParameters']['event'] == 'info':
        res = pull_info(username)
    return {
        'statusCode': 200,
        'body': json.dumps(res),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
