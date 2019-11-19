import os


class Config:
    SECRET_KEY = 'superkey'
    PG_USER = 'cursor'
    PG_PASSWORD = 'very_secret_password'
    PG_HOST = 'localhost'
    PG_PORT = 5432
    DB_NAME = 'book_exchange_db'
    SQLALCHEMY_DATABASE_URI = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    pass


class DevConfig:
    pass


def get_config():
    if os.environ.get('ENV') == 'TEST':
        return TestConfig
    elif os.environ.get('ENV') == 'DEV':
        return DevConfig
    return Config