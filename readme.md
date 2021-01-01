# CodeHub

CodeHub is a question answer web application.

## Requirements
```Run
pip3 install -r requirements.txt
```

## Setting Enviroment Variables
enviroment variables need to be defined in the terminal before app is run
copy and past the abose commands. Change the values in ' '

```python
"----------------ENV VARS----------------"
*each command has to be inserted separatly*
*admin account only created when home is accessed for the first time*

export SECRET_KEY='the_secret_key'
export SECURITY_PASSWORD_SALT='the_password_salt'

export MAIL_USERNAME='email_username'
export MAIL_PASSWORD='email_password'
export MAIL_DEFAULT_SENDER='full_email'

export SEED_ADMIN_EMAIL='admin_email' 
export SEED_ADMIN_PASSWORD='admin_password' 
```

## Run
navigate to project directory 
```Run
python3 run.py
```