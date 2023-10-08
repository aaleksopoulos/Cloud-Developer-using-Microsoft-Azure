import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="project3-dbserver.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="project3user@project3-dbserver" #TODO: Update value
    POSTGRES_PW="Ab1234!!"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://project3-ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=sauBh31Y0vTt+Cdi+OOXM4u3AD4rDQOuoFhay0KP9bY=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    # ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    # SENDGRID_API_KEY = '' #Configuration not required, required SendGrid Account
    ADMIN_EMAIL_ADDRESS= 'athanasios_al@hotmail.com'
    SENDGRID_API_KEY = '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' 

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False