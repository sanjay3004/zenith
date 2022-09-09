import os

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']

JWT_ACCESS_TOKEN_TIME_OUT_IN_MINUTES = int(os.environ['JWT_ACCESS_TOKEN_TIME_OUT_IN_MINUTES'])
JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES = int(os.environ['JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES'])

ENABLE_AUTH = False


class Config(object):
    CSRF_ENABLED = True
    """
    Common configurations
    """
    FIXED_RATE = 000
    URL_PREFIX = 'api'


class DevelopmentConfig(Config):
    # pymysql - for pip install pymysql || mysql-python not needed
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:iphone21@localhost/hoi'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:iphone21@127.0.0.1:5432/adrenaline'

    SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.environ['POSTGRES_USER'] + ':' + os.environ['POSTGRES_PASS'] + '@' + \
                              os.environ['POSTGRES_HOST'] + ':' + os.environ['POSTGRES_PORT'] + '/' + os.environ[
                                  'POSTGRES_DB']
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_TRACK_MODIFICATIONS=True
    DEVELOPMENT = True
    DEBUG = True
    FIXED_RATE = 200


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:iphone21@127.0.0.1:5432/adrenaline'
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.environ['POSTGRES_USER'] + ':' + os.environ['POSTGRES_PASS'] + '@' + \
                              os.environ['POSTGRES_HOST'] + ':' + os.environ['POSTGRES_PORT'] + '/' + os.environ[
                                  'POSTGRES_DB']
    SECRET_KEY = os.environ['SECRET_KEY']
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    FIXED_RATE = 300


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
"""
app= Flask(__name__)
app.config['MAIL_SERVER'] = 'smt.gmail.com'
app.config['MAIL_port'] = 465
app.config['MAIL_USER_SSL'] = True
app.config['MAIL_USERNAME'] = 'kurubaram9177@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
mail= Mail(app)

msg= Message()
msg.subject = "http://localhost:4018/set-password?email={email}"
msg.recipients = ['kurubaram9177@gmail.com']
msg.sender = 'username@gmail.com'
msg.body = 'localhost:5000/api/v1/users/set_Password'
mail.send(msg)




    #SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.getenv('POSTGRES_USER'] + ':' + os.getenv('POSTGRES_PASS'] + '@' + \os.getenv('POSTGRES_HOST'] + ':' + os.getenv('POSTGRES_PORT'] + '/' + os.getenv(
                                  'POSTGRES_DB']     """