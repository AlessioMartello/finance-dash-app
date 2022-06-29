from helpers.getfinancialData import getBalances
from dotenv import load_dotenv
import pandas as pd
import os


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
        balance.append(int(round(value, 0)))
        value -= i

    df["balance"] = balance

    return df


def removeErrorTransaction(df):
    """There is an error in the data from the API, to be cleaned. This does not exist in my account"""
    df = df[df["name"] != "REGULAR TRANSFER FROM MR ALESSIO RICARDO MARTELLO REFERENCE - RENT"]
    return df

if __name__ == '__main__':
    pass
