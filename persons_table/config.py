import os

POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")  # Change to your settings
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")  # Change to your settings
POSTGRES_DB_NAME = "flasksql"  # Change to your settings
ENTRIES_PER_PAGE = 300


class Config:
    SECRET_KEY = "any-string-to-keep-in secret"  # Change to your settings
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
