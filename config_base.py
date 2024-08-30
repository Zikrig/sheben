import os
from dotenv import load_dotenv

load_dotenv()

mysqldata={
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME")
}

admins = [
    '184374602',
    '1043157995'
]


picdir = os.getcwd() + '/data/'