# [AudioBid](https://audiobid.herokuapp.com/)

## Installation
### Initial Project Setup
1. Clone the Repository
2. Install Python
3. Go to Project Folder and run virtual env: `py -3 -m venv .venv`, `.venv\scripts\activate`
4. Install Django in virtual env: `python -m pip install --upgrade pip`, `python -m pip install django`
5. Or pip install -r requirements.txt
6. Follow the Database Setup Instruction
7. To create migrations: `python manage.py makemigrations`, `python manage.py migrate`
8. To make static files load, run : `python manage.py collectstatic`
9. To run the application: `python manage.py runserver`
### PostgressSQL Database Setup
1. Install PostgressSQL from: [Download Link](https://www.enterprisedb.com/postgresql-tutorial-resources-training?uuid=db55e32d-e9f0-4d7c-9aef-b17d01210704&campaignId=7012J000001NhszQAC)
2. Run application pgAdmin
3. Create a Database : `audiobidDB` under Databases
4. Enter all the DB Details in the `.env` file
5. If migrations give error, trying changing password in the .env file to the one that you set when you started the pgAdmin application.
### Google OAuth Setup
1. If you have existing DB, delete it
2. Run migration commands
3. Create new DB and new super user `python manage.py createsuperuser`
4. Login to admin
5. Make sure User, Sites and Social Accounts Tabs are visible
6. Click on Sites, delete Example.com, add site `127.0.0.1:8000`
7. Click on save and add another site `localhost:8000`
8. Click on Social Applications, then add social application
9. Set Provide as `google`, Name as `Google_Oauth` and get Client ID and Secret
10. Move all the available sites to chosen sites and click on Save
11. If after this you get error `Site Matching Query does not exist` on using Google Auth, try incrementing Site_ID by 1, until error goes away
### AWS S3
1. Create a bucket with an S3-access IAM role
2. Set necessary parameters in .env file
### LOGGING
1. To enable logging, uncomment the Logging code in env file and set DEBUG = True
2. To use logger to log details, add this lines to the top of your file:<br />
    `import logging`<br />
    `logger = logging.getLogger(__name__)`
3. To use it, write `logger.debug('Add what you want to print')`
### Deployment
1. Create an account on Heroku
2. Install Heroku CLI
3. Go to project directory in Terminal and use command `heroku login` and follow the steps as instructed
4. Use command `heroku create audiobid` to create an app on Heroku
5. Add env variables to heroku using command: `heroku config:set env_variable_name=env_variable_value`
6. Run `git push heroku main` to push your code to heroku
7. Run `heroku python3 manage.py migrate` to set the db
8. Create a superuser using the command `heroku python3 manage.py createsuperuser` and follow the instructions on screen
9. To open the deployed app, run `heroku open` and it will open the deployed app in the default web browser
10. To setup google auth use the steps present above
