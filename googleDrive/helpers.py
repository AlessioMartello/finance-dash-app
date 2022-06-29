from __future__ import print_function
import io
import json
from googleapiclient import http
from googleapiclient.discovery import build
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import os
#from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

import sys
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
serviceCredentialDict, keys = {}, ["type", "project_id", "private_key_id","private_key", "client_email", "client_id", "auth_uri", "token_uri", "auth_provider_x509_cert_url"]

for i in keys:
    serviceCredentialDict[i] = os.environ.get(i).replace("\\n", "\n")

sys.stdout.flush()
# Authenticate to Google Drive API
creds= service_account.Credentials.from_service_account_info(serviceCredentialDict)
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
    service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

def deleteFile(fileDelete):
    print("in the delete function: " +fileDelete)
    print("in the delete function: " +str(file_objs))

    service.files().delete(fileId=fileDelete).execute()
    service.files().emptyTrash().execute()

# todo this transactions not working in heroku but it is in helpers.py
def appendTransactions(newData: list):
    """Update the transaction file in google Drive"""
    # file_id= chooseFileId("transactions.json")

    # listExistingData=json.load(getFile(file_id))
    existingTransactionIds = [i["transaction_id"].strip("\'") for i in listExistingData]

    for transaction in reversed(newData):
        if transaction["name"] == "REGULAR TRANSFER FROM MR ALESSIO RICARDO MARTELLO REFERENCE - RENT":
            continue
        elif transaction["transaction_id"] not in existingTransactionIds:
            transaction["amount"] = -transaction["amount"]
            listExistingData.insert(0, transaction)
    try:
        deleteFile(transactions_file_id)  # todo this may change every time you call it?? in heroku
        print("successfully deleted transactions")
    except:
        print("error deleting transactions")
    try:
        uploadFile("transactions.json", listExistingData)
        print("successfully uploaded new transactions")
    except:
        print("error uploading transactions")

service = createConnection()
file_objs = getFileNames(service)
transactions_file_id = chooseFileId("transactions.json")
listExistingData=json.load(getFile(transactions_file_id))
print("outside of the append function: "+str(file_objs))
print("outside of the append function: "+chooseFileId("transactions.json"))
transactions = pd.read_json(getFile(chooseFileId("transactions.json")))
transactions_sample = pd.read_json(getFile(chooseFileId("transactions - Copy.json")))
creditScoreJsonStr = pd.read_json(getFile(chooseFileId("creditScore.json")))
balances_sample = pd.read_csv(getFile(chooseFileId("balancesexpo.csv")))


if __name__ == "__main__":
    print(service.files().get(fileId=chooseFileId("transactions.json"), fields='*').execute())
