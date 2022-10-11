# Audio-Bid

## Installation
### Initial Project Setup
1. Clone the Repository
2. Install Python
3. Go to Project Folder and run virtual env: `py -3 -m venv .venv`, `.venv\scripts\activate`
4. Install Django in virtual env: `python -m pip install --upgrade pip`, `python -m pip install django`
5. Follow the Database Setup Instruction
6. To create migrations: `python manage.py makemigrations`, `python manage.py migrate`
7. To run the application: `python manage.py runserver`
### PostgressSQL Database Setup
1. Install PostgressSQL from: [Download Link](https://www.enterprisedb.com/postgresql-tutorial-resources-training?uuid=db55e32d-e9f0-4d7c-9aef-b17d01210704&campaignId=7012J000001NhszQAC)
2. Run application pgAdmin
3. Create a Database : `audiobiDB` under Databases
4. If migrations give error, trying changing password in the settings.py to the one that you set when you started the pgAdmin application.
