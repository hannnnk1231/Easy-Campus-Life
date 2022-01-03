import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
def joinGroup(username, w_id, g_id):
      response = requests.get(HOST+'workspace_group/_search?q=username:{}&size=10000'.format(username), auth=awsauth, headers={'Content-type': 'application/json'})
      u_id = [str(u["_id"]) for u in json.loads(response.text)['hits']['hits'] if u["_source"]['w_id']==w_id][0]
      body = {
        "doc": {
          'g_id': g_id,
          'w_id': w_id,
          'username': username
        }
      }
      response = requests.post(HOST+'workspace_group/_update/'+u_id, auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
      print(response.text)
      return "success"
     
    
def lambda_handler(event, context):
    # TODO implement
    response = joinGroup(event['username'], event['w_id'], event['g_id'])
    return {
        'statusCode': 200,
        'body': response,
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
