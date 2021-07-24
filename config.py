class Config:
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = "Secret Key"
    ADMIN_KEY = "Admin Key"
    DATABASE_URI = "postgresql://postgres:password@localhost/databasename"

class TestingConfig(Config):
    DEBUG = True
    SECRET_KEY = "Secret Key"
    ADMIN_KEY = "Admin Key"
    DATABASE_URI = "postgresql://postgres:password@localhost/databasename"