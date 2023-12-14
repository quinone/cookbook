# CookBook


Developed by Eoghan Quinn
Student number: 12475528

CookBook is a Flask application that allows users submit recipes online and store them.
Users can then view their own and others public recipes. 
Thank you for reading and installing CookBook.


## Initial  Setup

Open CookBook folder in pycharm.

Allow pycharm to create a new virtual environment called venv.

Install the packages from requirements.txt file.

Using the terminal window of pycharm enter:

```bash
export FLASK_APP=cookbook.py
```

This updates the environment variable for FLASK_APP. 
Allowing the app to be ran with the command:

```bash
flask run
```

Debug can be enabled by adding:

```bash
flask run --debug
```

The application should now be available locally at http://127.0.0.1:5000.

The application can be stopped using CTRL + C.

Adding the hosting arguement can make the application available over your local network: 

```bash
flask run --host 0.0.0.0
```


## Flask shell

Flask shell can be used to execute commands.

The shell command is:

```bash
flask shell
```


## Database 

To create all tables the following command can be entered in the shell:

```bash
db.session.create_all()
db.session.commit()
```

The current tables in the database can be deleted/dropped by:

```bash
db.session.drop_all()
db.session.commit()
```


## Sample info

The recipes.py file contains sample users and recipes.
These can be entered in to a new database by entering the following in the shell:

```bash
from app.recipes import add_all_recipes, add_all_users
add_all_users()
add_all_recipes()
```


## Using Email service

Due to recent security update by gmail the email account must generate a third party password through gmails security panel. See https://support.google.com/mail/answer/185833?hl=en for details on setting up your own account. 

For the purpose of demonstrating the application the project has a file containing the login details for a demo gmail account. In order to get the emails to send correctly the MAIL_USERNAME, MAIL_PASSWORD and COOKBOOK_ADMIN environment variables must be exported. This can be done using the following commands:

```bash
export MAIL_USERNAME=<Development email>
export MAIL_PASSWORD=<Development password>
export COOKBOOK_ADMIN=<Development email>
```

Commands available in emailauth.txt file.





