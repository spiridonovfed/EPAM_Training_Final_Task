import os

POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")  # Change to your settings
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")  # Change to your settings
POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME")  # Change to your settings
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")  # Change to your settings
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")  # Change to your settings
ENTRIES_PER_PAGE = 300


class Config:
    SECRET_KEY = "any-string-to-keep-in secret"  # Change to your settings
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
        f"{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    )  # Change to your settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
