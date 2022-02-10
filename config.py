from os import getenv


class Config(object):
    DEBUG_MODE = getenv("DEBUG_MODE", True)
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
