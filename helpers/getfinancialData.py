import plaid
from plaid.api import plaid_api
import os
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
import datetime
from dotenv import load_dotenv
from pathlib import Path


root = Path(__file__).parent.parent
load_dotenv()

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': os.getenv("PLAID_CLIENT_ID"),
        'secret': os.getenv("PLAID_SECRET"),
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


def getTransactions(todayDate):
    """Return the transactions as a plaid object"""
    request = TransactionsGetRequest(
        access_token=os.getenv("DEV_ACCESS_TOKEN"),
        start_date=datetime.date(2020,1,1),
        end_date= todayDate,
        options=TransactionsGetRequestOptions(count=500)
    )
    response = client.transactions_get(request)
    transactions = response['transactions']
    return transactions


def getBalances(accessToken):
    """Return the balances as a plaid object"""
    request = AccountsBalanceGetRequest(access_token=accessToken)
    response = client.accounts_balance_get(request)
    accounts = response['accounts']
    return accounts

def backupTransactions():
    pass
    # shutil.copy(getFile(chooseFileId("transactions.json")), getFile(chooseFileId("transactions - Copy.json")))
    # todo change this to be in google drive

if __name__ == '__main__':
    pass