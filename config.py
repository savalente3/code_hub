
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

