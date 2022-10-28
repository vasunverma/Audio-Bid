# Audio-Bid

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

