import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DB_CON_STR = os.getenv('DB_CON_STR')

DOCUMENT_DIR = os.getenv("DOCUMENT_DIR")

IS_DEV_ENV = int(os.getenv('IS_DEV_ENV'))

REDIS_HOST = os.getenv('REDIS_HOST')

REDIS_PORT = os.getenv('REDIS_PORT')
