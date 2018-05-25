# Setup instructions


## Setup and start backend
* Install python3 (easiest way is to install through Homebrew: http://docs.python-guide.org/en/latest/starting/install3/osx/)
* Install virtualenv (Installation instructions: https://virtualenv.pypa.io/en/stable/installation/)
* Clone repository
  * `git clone https://github.com/ravipunj/se-challenge-payroll.git; cd se-challenge-payroll`
* Activate virtual environment
  * `source payrollenv/bin/activate`
* Install pip dependencies
  * `pip install -r requirements.txt`
* Initialize sqlite database (the database is created at _/tmp/payroll.db_)
  * `flask db init`
* Run all database migrations
  * `flask db upgrade`
* Run API server
  * `gunicorn --bind 0.0.0.0:8000 app:app`

## Setup and launch frontend
* Install NodeJS (https://www.dyclassroom.com/howto-mac/how-to-install-nodejs-and-npm-on-mac-using-homebrew)
* Go to frontend app folder
  * `cd payroll-app`
* Install dependencies
  * `npm install`
* Follow one of the two methods to run the frontend app
  * Method #1: This will launch the frontend app in a nodejs server
    * `npm start`
  * Method #2: This will bundle the frontend app into static files
    * `npm run build`
    * Open _payroll-app/build/index.html_ in a browser

# Test Instructions

## Flask App testing
From _\<repo root\>_, run `python3 -m nose`

## React App testing
From _\<repo root\>/payroll-app, run `npm test`
  