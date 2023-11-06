from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/audiohub"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@postgres:5432/audiohub"
"""
# local fix
host_server = "audiohub.postgres.database.azure.com"
db_server_port = "5432"
database_name = "fastapi"
db_username = "audiohubadmin@audiohub"
db_password = "#123456789F4"
ssl_mode = "prefer"
"""

# deployment
host_server = os.environ.get('host_server', 'aduio-hub-server.postgres.database.azure.com')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'aduio-hub-database')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'jvzwvrtzkk')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', '587KW8MXN2B64IM7$')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','require')))

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
