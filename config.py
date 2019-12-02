class Config:
    pass


class TestConfig:
    SECRET_KEY = 'superkey_test'
    PG_USER = 'cursor'
    PG_PASSWORD = 'very_secret_password'
    PG_HOST = 'localhost'
    PG_PORT = 5432
    DB_NAME = 'book_exchange_test_db'
    SQLALCHEMY_DATABASE_URI = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig:
    SECRET_KEY = 'superkey'
    PG_USER = 'cursor'
    PG_PASSWORD = 'very_secret_password'
    PG_HOST = 'localhost'
    PG_PORT = 5432
    DB_NAME = 'book_exchange_db'
    SQLALCHEMY_DATABASE_URI = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_config(env=None):
    if env == 'TEST':
        return TestConfig
    elif env == 'DEV':
        return DevConfig
    return Config
