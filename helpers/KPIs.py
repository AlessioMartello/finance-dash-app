import pandas as pd

relevantCols = ["name", "amount", "datetime", "transaction_code"]


def averageSpend(df):
    """Returns the average expenditure under £100"""
    spendsUnderOneHundred = df[(df["amount"] < 0) & (df["amount"] > -100)]["amount"]
    mean = spendsUnderOneHundred.mean()
    median = spendsUnderOneHundred.median()
    mode = spendsUnderOneHundred.round().mode()
    return mean, median, mode.values[0]  # average spend under £100


def getCategoryCounts(df):
    """Gets the counts of the categories, for expenditures less than £100"""
    category_lst = [j.strip("\" \'") for i in df[df["amount"] < 0]["category"].tolist() for j in i]
    counts = {item: category_lst.count(item) for item in category_lst}
    cat, cnt = [], []
    for k, v in counts.items():
        cat.append(k)
        cnt.append(int(v))

    the_dict = {"categories": cat, "Counts": cnt}
    df = pd.DataFrame(the_dict)

    topTen = df.nlargest(10, "Counts")
    return topTen


def monthlyExpenditure(rawTransactions):
    """Get the expenditures per month, excluding recurring payments"""
    for col in ['datetime', "date"]:
        rawTransactions[col] = pd.to_datetime(rawTransactions[col])
    TransactionsAdHoc = notRecurring(rawTransactions)
    spendings = TransactionsAdHoc[TransactionsAdHoc["amount"] < 0]
    spendingsGrouped = spendings[["date", "amount"]].groupby(
        pd.Grouper(key="date", freq='M')).sum().reset_index().round()
    spendingsGrouped["date"] = spendingsGrouped["date"].dt.strftime('%d-%m-%Y')
    spendingsGrouped["4 Month Rolling Average"] = spendingsGrouped.rolling(4).mean()
    return spendingsGrouped


def currentMonthTransactions(transDf):
    """Filters the df to be of the current month only: returns a df"""
    year = transDf["datetime"].max().year
    month = transDf["datetime"].max().month

    transactionsThisMonth = transDf[(transDf["datetime"].dt.month == month) &
                                    (transDf["datetime"].dt.year == year)
                                    ][relevantCols]
    return transactionsThisMonth


def notRecurring(df):
    """Function to clean a df of recurring payments"""
    df = df[(df["amount"] != -1900) &
            (df["amount"] != -500) &
            (df["transaction_code"] != "direct debit") &
            (df["transaction_code"] != "standing order") &
            (df["amount"] > -10000)  # Assume expenditures arent greater than £10,000
            ]
    return df


def thisMonthSpend(df):
    """Returns the value of the expenditure this month"""
    transactionsThisMonth = notRecurring(df)
    spentThisMonth = transactionsThisMonth[(transactionsThisMonth["amount"] < 0)]["amount"].sum()
    return spentThisMonth


def getTenLargestBuys(df):
    """Returns a ranked df of the ten largest expenditures/ It groups the merchant if it is recurring"""
    df = notRecurring(df)
    count = 10
    expenses = df[df["amount"] < 0]
    expensesGrouped = expenses.groupby(["name"])["amount"].sum().reset_index()
    tenLargestBuys = expensesGrouped.nsmallest(n=count, columns=['amount'])
    newidx = tenLargestBuys.reset_index(drop=True).index
    newidx += 1
    tenLargestBuys.insert(loc=0, column="#", value=newidx)
    return tenLargestBuys


if __name__ == '__main__':
    df = getCategoryCounts(pd.read_csv("transexpo.csv"))
    print(df)
