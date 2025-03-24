# Live at https://cybercraft-bangladesh.vercel.app/

# Instructions to run this project on the local computer

Clone or download the repository

- Open project directory and open command prompt, then create and activate virtual environment.
- Go to directory where manage.py file exists.
- Visit the .env.dev file and setup the variables, then rename the file to .env.local
- Run the below command to Install necessary libraries

```bash
pip install -r requirements.txt
```

- Run the below commands to apply migrations

```bash
py manage.py makemigrations app_useraccount
py manage.py migrate
py manage.py makemigrations app_customer
py manage.py migrate
```

- Create super user/admin user:

```bash
py manage.py createsuperuser
```

- Run backend server

```bash
py manage.py runserver
```

### Note:

Make sure the front-end is setup. If not please visit the repo at https://github.com/Hadayetullah/cybercraft-bangladesh-frontend and see the readme instruction.
