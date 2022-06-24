from __future__ import print_function
import io
import json
from googleapiclient import http
from googleapiclient.discovery import build
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import os
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
serviceCredentialDict, keys = {}, ["type", "project_id", "private_key_id","private_key", "client_email", "client_id", "auth_uri", "token_uri", "auth_provider_x509_cert_url"]

for i in keys:
    serviceCredentialDict[i] = os.environ.get(i)

# Authenticate to Google Drive API
creds= ServiceAccountCredentials.from_json_keyfile_dict(serviceCredentialDict, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)
results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()

def createConnection():
    service = build('drive', 'v3', credentials=creds)
    return service


def getFileNames(service):
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


def getFile(file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh


def chooseFileId(name):
    for i in file_objs:
        if i["name"] == name:
            return i["id"]


def uploadFile(name, content):
    media = http.MediaIoBaseUpload(io.StringIO(json.dumps(content, default=str)), mimetype='plain/text')
    file_metadata = {'name': name}
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

def deleteFile(fileDelete):
    file = service.files().delete(fileId=fileDelete).execute()

service = createConnection()
file_objs = getFileNames(service)


transactions = pd.read_json(getFile(chooseFileId("transactions.json")))
transactions_sample = pd.read_json(getFile(chooseFileId("transactions - Copy.json")))
creditScoreJsonStr = pd.read_json(getFile(chooseFileId("creditScore.json")))
balances_sample = pd.read_csv(getFile(chooseFileId("balancesexpo.csv")))


if __name__ == "__main__":
    pass