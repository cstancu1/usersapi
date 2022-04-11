import os

DEBUG=os.getenv("DEBUG", False)
TITLE=os.getenv("TITLE", False)
VERSION=os.getenv("VERSION", '0.0.0')
DEPLOY=os.getenv("DEPLOY_MODE", "prod")
PASSWORD_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
JWT_PRIVATE_KEY = open(os.getenv("JWT_PRIVATE_KEY", ""), "rb").read()
JWT_PUBLIC_KEY = open(os.getenv("JWT_PUBLIC_KEY", ""), "rb").read()
JWT_DEFAULT_EXP_MIN = 30
MONGO_USER = os.getenv("MONGO_USER", "USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "PASS")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "users")
SURVEYS_API_URL = os.getenv("SURVEYS_API_URL")