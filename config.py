
# #GET SCRET_KEY
# #python interpreter -> python on terminal
# #import secrets
# #>>> secrets.token_hex(16)
# app.config['SECRET_KEY'] = '44f243fc1815933976c3d57cb97eb2dd'


"""Base config."""
STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'
SECRET_KEY = '44f243fc1815933976c3d57cb97eb2dd'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SECURITY_PASSWORD_SALT = 'hellohello'

 # mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = 'sa.valente3'
MAIL_PASSWORD = 'Astyop158'
MAIL_DEFAULT_SENDER = 'sa.valente3@gmail.com'

 
