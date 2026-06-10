import os
import boto3
import sqlalchemy
import pandas as pd


class Settings:
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    S3_URL = os.getenv("S3_URL")
    S3_USER = os.getenv("S3_USER")
    S3_PASSWORD = os.getenv("S3_PASSWORD")

    BUCKET_NAME = "hse-data"

    @property
    def DB_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
    @property
    def S3_CLIENT(self):
        return boto3.client(
            "s3",
            endpoint_url=self.S3_URL,
            aws_access_key_id=self.S3_USER,
            aws_secret_access_key=self.S3_PASSWORD,
        )


settings = Settings()

engine = sqlalchemy.create_engine(settings.DB_URL)

s3_client = settings.S3_CLIENT


