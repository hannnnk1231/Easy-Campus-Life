import json
import boto3
import requests
import uuid
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
def createWorkspace(workspaceName, username):
    response = requests.post(HOST+'workspaces/_doc/', auth=awsauth, data=json.dumps({'workspaceName': workspaceName}), headers={'Content-type': 'application/json'})
    w_id = json.loads(response.text)['_id']
    body = {
        'workspaceName': workspaceName,
        'w_id': w_id,
        'username': username
    }
    response = requests.post(HOST+'workspace_user/_doc/', auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
    body = {
        'w_id': w_id,
        'username': username,
        'g_id': str(uuid.uuid4())
    }
    response = requests.post(HOST+'workspace_group/_doc/', auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
    return w_id

def joinWorkspace(w_id, username):
    response = requests.get(HOST+'workspaces/_search?q=_id:{}'.format(w_id), auth=awsauth, headers={'Content-type': 'application/json'})
    workspace = json.loads(response.text)['hits']['hits']
    if not workspace:
        return "Workspace does not exist"
    else:
        workspaceName = workspace[0]["_source"]['workspaceName']
        response = requests.get(HOST+'workspace_user/_search?q=username:{}&size=10000'.format(username), auth=awsauth, headers={'Content-type': 'application/json'})
        workspace = [w["_source"] for w in json.loads(response.text)['hits']['hits'] if w["_source"]['w_id']==w_id]
        if not workspace:
            body = {
                'workspaceName': workspaceName,
                'w_id': w_id,
                'username': username
            }
            response = requests.post(HOST+'workspace_user/_doc/', auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
            body = {
                'w_id': w_id,
                'username': username,
                'g_id': str(uuid.uuid4())
            }
            response = requests.post(HOST+'workspace_group/_doc/', auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
            return "success"
        else:
            return "User already in workspace: "+workspaceName
    
def lambda_handler(event, context):
    # TODO implement
    if event['event'] == "create":
        response = createWorkspace(event["workspaceName"], event["username"])
    else:
        response = joinWorkspace(event["w_id"], event["username"])
        
    return {
        'statusCode': 200,
        'body': response,
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
