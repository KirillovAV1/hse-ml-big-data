import boto3
import sqlalchemy
import pandas as pd
from io import StringIO, BytesIO
from common.connections import engine, s3_client, settings


def extract_df_from_db(table_name: str) -> pd.DataFrame:
    with engine.begin() as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    return df

def extract_csv_from_s3(table_name: str, prefix: str) -> pd.DataFrame:
    path = f"{prefix}/{table_name}/"

    response = s3_client.list_objects_v2(
        Bucket=settings.BUCKET_NAME,
        Prefix=path
    )

    dfs = []

    for obj in response.get("Contents", []):
        key = obj["Key"]

        if not key.endswith(".csv"):
            continue

        file_response = s3_client.get_object(
            Bucket=settings.BUCKET_NAME,
            Key=key
        )

        df_part = pd.read_csv(BytesIO(file_response["Body"].read()))
        dfs.append(df_part)


    return pd.concat(dfs, ignore_index=True)


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