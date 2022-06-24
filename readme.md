# Alessio's Financial Planner Web App

This is a Python-built financial planner for importing, analysing and reporting on my finances.

###How it works

Bank Transactions and balances are extracted via the [Plaid](https://plaid.com/en-gb/) open banking API.
Data is transformed and manipulated using Pandas. KPIS are calculated and reported on using [Dash](https://plotly.com/dash/). The report is currently hosted locally.

## Installation
Firstly clone the repository. \
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install requirements.txt
```

Create a .env file to store the following variables:
* DEV_ACCESS_TOKEN
* PLAID_CLIENT_ID
* PLAID_SECRET

In order to obtain the DEV_ACCESS_TOKEN, create a plaid account and then follow the procedure outlined here in the [Plaid Quickstart Guide](https://github.com/plaid/quickstart).

Following this update your environment variables and execute dashboard.py
##Usage
#####Key KPIS that are returned include:
* Average spend
* Monthly expenditure
* Transactions history with filtering capabilities
* Expenditure category counts


## Notes
This is a bespoke tool. Modifications will be needed to configure this to work with other banks.

## Planned development
The intention is to host this on Heroku with a login on top. Such that it can be accessed via the web, on a mobile device.
Following this, an Android App will be used as the UI.

## Contributing
Pull requests are welcome.

## Contact
[LinkedIn](https://www.linkedin.com/in/alessiomartello/)

## License
[MIT](https://choosealicense.com/licenses/mit/)