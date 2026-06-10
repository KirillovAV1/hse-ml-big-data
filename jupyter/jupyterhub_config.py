import os

c = get_config()

c.Authenticator.allow_all = True

c.Spawner.environment = {
    "DB_HOST": os.environ.get("DB_HOST"),
    "DB_PORT": os.environ.get("DB_PORT"),
    "DB_NAME": os.environ.get("DB_NAME"),
    "DB_USER": os.environ.get("DB_USER"),
    "DB_PASSWORD": os.environ.get("DB_PASSWORD"),

    "S3_URL": os.environ.get("S3_URL"),
    "S3_USER": os.environ.get("S3_USER"),
    "S3_PASSWORD": os.environ.get("S3_PASSWORD")
}