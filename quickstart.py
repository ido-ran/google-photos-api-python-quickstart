"""
Shows basic usage of the Photos v1 API.

Creates a Photos v1 API service and prints the names and ids of the last 10 albums
the user has access to.
"""
from __future__ import print_function
import os 
import pickle
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_httplib2  # This gotta be installed for build() to work

# Setup the Photo v1 API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
creds = None
if(os.path.exists("token.pickle")):
    with open("token.pickle", "rb") as tokenFile:
        creds = pickle.load(tokenFile)
if not creds or not creds.valid:
    if (creds and creds.expired and creds.refresh_token):
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port = 0)
    with open("token.pickle", "wb") as tokenFile:
        pickle.dump(creds, tokenFile)
service = build('photoslibrary', 'v1', credentials = creds)

# Call the Photo v1 API
results = service.albums().list(
    pageSize=10, fields="nextPageToken,albums(id,title)").execute()
items = results.get('albums', [])
if not items:
    print('No albums found.')
else:
    print('Albums:')
    for item in items:
        print('{0} ({1})'.format(item['title'].encode('utf8'), item['id']))
