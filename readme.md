# CodeHub

CodeHub is a question answer web application.
The exponential growth and dependency of web applications is leading to more personal information being stored and used by these systems. Therefore, security is now essential when designing websites, apps and software. In this project a simple and secure message board web application was developed that allows users to ask and answer questions related to programming. There are a lot of factors that can compromise the security of a website; thus, protection measures and protocols must be implemented to protect them from being accessed by unauthorized people and later causing data breaches in the system.

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
