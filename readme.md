# Alessio's Financial Planner Web App

This is a Python-built financial planner for importing, analysing and reporting on my finances.

### See it in action!
See the working web application [here!](https://alessio-finance-dash-app.herokuapp.com/live)

When prompted enter the "test" for both security parameters to see sample data.
### How it works

Bank Transactions and balances are extracted via the [Plaid](https://plaid.com/en-gb/) open banking API.
Data is transformed and manipulated using Pandas. KPIS are calculated and reported on using [Dash](https://plotly.com/dash/). The data is stored securely using Google Drive and accessed via its [API](https://developers.google.com/drive/api) using a service  with each run of the app.
The application is hosted in [Heroku](https://dashboard.heroku.com/).

![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/45970352/176474976-eeb77e66-730b-49e3-aebf-eef7ba3dbde5.gif)

## Usage
##### Key KPIS that are returned include:
* Average spend
* Monthly expenditure
* Transactions history with filtering capabilities
* Expenditure category counts
* Ten largest expenditures this month
* Current balance


## Notes
This is a bespoke tool. Modifications will be needed to configure this to work with other banks.

## Planned development
The intention is to create an Android App will be used as the UI.

## Contributing
Pull requests are welcome.

## Contact
[LinkedIn](https://www.linkedin.com/in/alessiomartello/)

## License
[MIT](https://choosealicense.com/licenses/mit/)