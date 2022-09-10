from __future__ import print_function
import io
from googleapiclient import http
from googleapiclient.discovery import build
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload
import os
from google.oauth2 import service_account
import string
import random
import json
import sys

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
serviceCredentialDict, keys = {}, ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id",
                                   "auth_uri", "token_uri", "auth_provider_x509_cert_url"]

for i in keys:
    serviceCredentialDict[i] = os.environ.get(i).replace("\\n", "\n")

sys.stdout.flush()
creds = service_account.Credentials.from_service_account_info(serviceCredentialDict)  # Authenticate to Google Drive API
service = build('drive', 'v3', credentials=creds)
results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()


def createConnection():
    """Connects to Google Drive use service account credentials"""
    service = build('drive', 'v3', credentials=creds)
    return service


def getFileNames(service):
    """Returns a list of the files in Google Drive and their unique ids"""
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


def getFile(file_id):
    """Downloads the chosen file from Google Drive API"""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh


def chooseFileId(name):
    """Uses the file name to extract the file id from the list of files"""
    for i in getFileNames(service):
        if i["name"] == name:
            return i["id"]


def uploadFile(name, content):
    """Uploads the file to Google Drive via its API using a service account"""
    media = http.MediaIoBaseUpload(io.StringIO(json.dumps(content, default=str)), mimetype='plain/text')
    file_metadata = {'name': name}
    service.files().create(body=file_metadata,
                           media_body=media,
                           fields='id').execute()


def deleteFile(fileDelete):
    """Deletes the file based on it'd id"""
    service.files().delete(fileId=fileDelete).execute()
    service.files().emptyTrash().execute()


def appendTransactions(newData: list):
    """Update the transaction file in google Drive"""
    transactions_file_id = chooseFileId("transactions.json")
    listExistingData = json.load(getFile(transactions_file_id))
    existingTransactionIds = [i["transaction_id"].strip("\'") for i in listExistingData]

    for transaction in reversed(newData):
        if transaction["name"] == "REGULAR TRANSFER FROM MR ALESSIO RICARDO MARTELLO REFERENCE - RENT" \
                or transaction["transaction_id"] == "Y87k5wPAgAF3a53Apr7xFpzaEEn0AqIzMMnpn": #errenous bank transfer to savings acc
            continue
        elif transaction["transaction_id"] not in existingTransactionIds:
            transaction["amount"] = -transaction["amount"]
            listExistingData.insert(0, transaction)
    try:
        deleteFile(transactions_file_id)  # todo this may change every time you call it?? in heroku
        print("successfully deleted transactions")
        uploadFile("transactions.json", listExistingData)
        print("successfully uploaded new transactions")
    except Exception as e:
        print(e)
        print("error deleting and uploading transactions")


def makeSampleData():
    """Generates sample data using the latest transactions"""
    letters = string.ascii_uppercase
    sourceDataId = chooseFileId("transactions.json")
    source_json = json.load(getFile(sourceDataId))

    for i in source_json:
        i["name"] = "Payment " + random.choice(letters)
        i["account_id"] = "Account id " + random.choice(letters)
        i["transaction_id"] = "Transaction id " + random.choice(letters)
        i["amount"] = random.randint(-1000, 1000)
    try:
        sinkDataId = chooseFileId("transactions - Copy.json")
        deleteFile(sinkDataId)
        print("Successfully deleted sample data")
    except Exception as e:
        print(e)
        print("error deleting sample data")
    try:
        uploadFile("transactions - Copy.json", source_json)
        print("successfully uploaded sample data")
    except Exception as e:
        print(e)
        print("error uploading sample data")


service = createConnection()

if __name__ == "__main__":
    print(getFileNames(service))