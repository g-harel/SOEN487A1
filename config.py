class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///SOEN487A1.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/SOEN487A1.sqlite"
