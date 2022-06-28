#from googleDrive.helpers import getFile,  deleteFile, uploadFile, listExistingData, transactions_file_id#,chooseFileId,
from helpers.getfinancialData import getBalances
from dotenv import load_dotenv
import pandas as pd
import os
#import string
#import random
#import json

load_dotenv()

accessToken = os.getenv("DEV_ACCESS_TOKEN")
currentAccountName = os.getenv("CURRENTACCOUNT")
balances = getBalances(accessToken)




def processBalances():
    """ Expand the nested json in the balances API response"""
    formattedBalances = list(map(lambda x: x.to_dict(), balances))
    df = pd.json_normalize(formattedBalances)
    return df


def processTransactions(transactions):
    """Make outgoing transactions negative"""
    formattedTransactions = list(map(lambda x: x.to_dict(), transactions))

    return formattedTransactions


def getHistoricBalances(df, df2):
    """Work back from the latest balance using historic transactions to get the balance history"""
    transactions = df["amount"].tolist()
    value = df2[df2["name"] == currentAccountName]["balances.available"].values[0]
    balance = []

    for i in transactions:
        balance.append(value)
        value -= i


    df["balance"] = balance

    return df

def removeErrorTransaction(df):
    """There is an error in the data from the API, to be cleaned. This does not exist in my account"""
    df = df[df["name"] != "REGULAR TRANSFER FROM MR ALESSIO RICARDO MARTELLO REFERENCE - RENT"]
    return df

# def makeSampleData(source_id, destination_id):
#
#     source = getFile(source_id)
#     letters = string.ascii_uppercase
#     source_json = source
#
#     for i in source_json:
#         i["name"] = "Payment " + random.choice(letters)
#         i["account_id"] = "Account id " + random.choice(letters)
#         i["transaction_id"] = "Transaction id " + random.choice(letters)
#         i["amount"] = random.randint(-1000, 1000)
#
#     deleteFile(destination_id)
#     uploadFile("transactions - Copy.json", source_json)

if __name__ == '__main__':
    pass