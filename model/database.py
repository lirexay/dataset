import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

import time


# MYSQL_USER = "root"
# MYSQL_PASSWORD = "password"
# MYSQL_HOST = "db"
# MYSQL_PORT = "3306"
# MYSQL_DATABASE = "kasra"

# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@db:3306/dataset"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@127.0.0.1:3308/dataset"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:G|yte11H_9&@127.0.0.1:3306/kasra"

time.sleep(15)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
