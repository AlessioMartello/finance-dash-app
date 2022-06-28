from googleDrive.helpers import transactions, transactions_sample, balances_sample, \
    appendTransactions,  uploadFile, transactions_file_id, listExistingData,deleteFile  # ,creditScoreJsonStr
from helpers.formatData import getHistoricBalances, removeErrorTransaction, processTransactions, processBalances#, appendTransactions
from helpers.KPIs import averageSpend, getCategoryCounts, monthlyExpenditure, currentMonthTransactions, thisMonthSpend
from helpers.getfinancialData import getTransactions
import pandas as pd
from datetime import date, timedelta
from helpers.dashboardHelpers import cleanCategories
from dotenv import load_dotenv

load_dotenv()

# Load in data
#creditScoreFile = creditScoreJsonStr
todayDate = date.today() + timedelta(days=1)
transRaw = getTransactions(todayDate)
listProcessedTransaction = processTransactions(transRaw)
appendTransactions(listProcessedTransaction)
deleteFile(transactions_file_id)  # todo change to update
uploadFile("transactions.json", listExistingData)

def getDisplayData(live=False):
    if live:
        transactionsFile = transactions
        balancesDf = processBalances()

    else:
        transactionsFile = transactions_sample
        balancesDf = balances_sample
    return transactionsFile, balancesDf


def getTransDf(transactionsFile, balancesDf):
    transDfUnclean = getHistoricBalances(removeErrorTransaction(transactionsFile), balancesDf)
    transDf = cleanCategories(transDfUnclean)
    return transDf

def getBalances(balancesDf):
    releventBalances = balancesDf[["name", "balances.current"]].round()
    return releventBalances

def getTransThisMonth(transDf):
    transThisMonth = currentMonthTransactions(transDf)
    return transThisMonth

def getText(transDf, transThisMonth):
    # Get KPIs
    kpiDict={}
    meanSpend, medianSpend, modeSpend = averageSpend(transDf)
    kpiDict["catgoryCounts"] = getCategoryCounts(transDf)
    kpiDict["monthlySpending"] = monthlyExpenditure(transDf)
    kpiDict["spentValue"] = thisMonthSpend(transThisMonth)

    # Define all text, headers and variables
    textDict={}
    minDate = pd.to_datetime(transDf["date"]).dt.date.min() - timedelta(days=1)
    textDict["KPIText"] = \
f'''#### Average Spend: £{round(abs(meanSpend))} 
#### Median Spend: £{round(abs(medianSpend))} 
#### Modal Spend: £{round(abs(modeSpend))}
*Expenditures under £100'''
    textDict["monthlySpendingText"] = \
f'''### Monthly spending totals 
##### excluding standing orders and direct debits'''
    textDict["balancesText"] = \
f"""### Account Balances 
##### Excluding ISA"""
    textDict["creditScoreText"] = f"""### Experian Credit Score over time"""
    textDict["pieChartText"] = f"""### Category frequency"""
    textDict["balanceHistoryText"] = f"""### Current account balance and transaction history"""
    textDict["thisMonthTransactionsTable"] = f"""### This month's transactions"""
    textDict["thisMonthTransactionsGraph"] = f"""### This month's transactions over time"""
    textDict["thisMonthSpent"] = f"""### Spent this month: £{round(abs(kpiDict["spentValue"]))}"""
    textDict["allTransactionsText"] = f"""### All transactions"""
    textDict["topTenText"] = f"""### Ten largest spending locations"""

    return textDict, kpiDict, minDate



if __name__ == '__main__':
    pass