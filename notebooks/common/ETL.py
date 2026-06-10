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


def load_partitioned_df_to_s3(
    df: pd.DataFrame,
    table_name: str,
    prefix: str,
    date_column: str,
) -> None:
    
    df[date_column] = pd.to_datetime(df[date_column]).dt.date

    for date_value, part_df in df.groupby(date_column):
        csv_buffer = StringIO()
        part_df.to_csv(csv_buffer, index=False)

        s3_client.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=f"{prefix}/{table_name}/{date_column}={date_value}/{table_name}.csv",
            Body=csv_buffer.getvalue()
        )