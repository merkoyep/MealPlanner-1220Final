"""Initialize Config class to access environment variables."""
from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    """Set environment variables."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'postgresql://postgres:5b2e05cd8c3526e3@merkoyep-final-project-db.dev.merkoyep.me:5432/postgres')
    SECRET_KEY = os.getenv('SECRET_KEY', 'itsasecret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
