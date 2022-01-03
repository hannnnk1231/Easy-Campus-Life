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

def searchES(w_id):
    response = requests.post(HOST+"workspace_group/_search?q=w_id:{}&size=10000".format(w_id), auth=awsauth, headers={"Content-Type":"application/json"})
    pairs = [w["_source"] for w in json.loads(response.text)['hits']['hits']]
    res = {}
    for p in pairs:
        if p['g_id'] not in res:
            res[p['g_id']] = [p['username']]
        else:
            res[p['g_id']].append(p['username'])
    print(res)
    return [{"g_id": key, "users": res[key]} for key in res]

def lambda_handler(event, context):
    # TODO implement
    w_id = event['queryStringParameters']['w_id']
    res = searchES(w_id)
    return {
        'statusCode': 200,
        'body': json.dumps(res),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
