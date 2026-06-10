import boto3
import sqlalchemy
import pandas as pd
from io import StringIO
from common.connections import engine, s3_client, settings


def extract_df_from_db(table_name: str) -> pd.DataFrame:
    with engine.begin() as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    return df


def load_df_to_s3(
        df: pd.DataFrame, 
        filename: str,
        prefix: str
    ):

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3_client.put_object(
        Bucket=settings.BUCKET_NAME,
        Key=f"{prefix}/{filename}.csv",
        Body=csv_buffer.getvalue()
    )

def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    pass