import boto3
import sqlalchemy
import pandas as pd
from io import StringIO, BytesIO
from pandas.api.types import is_numeric_dtype
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
    partition_dates = pd.to_datetime(df[date_column]).dt.date

    for date_value, part_df in df.groupby(partition_dates):
        csv_buffer = StringIO()
        part_df.to_csv(csv_buffer, index=False)

        s3_client.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=f"{prefix}/{table_name}/{date_column}={date_value}/{table_name}.csv",
            Body=csv_buffer.getvalue()
        )


def transforms_date_values(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df["date"] = df[date_column].dt.date

    return df


def transforms_null_values(df: pd.DataFrame) -> pd.DataFrame:
    columns_with_nulls = df.columns[df.isnull().any()]

    for column in columns_with_nulls:
        if is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna("Нет данных")

    return df


def transforms_outliers(df: pd.DataFrame) -> pd.DataFrame: 
    df = df.copy()
    skip_columns = {"downtime_hours"}

    for column in df.columns:
        if "_id" in column or column in skip_columns or not is_numeric_dtype(df[column]):
            continue

        Q1 = df[column].quantile(0.25) 
        Q3 = df[column].quantile(0.75) 
        IQR = Q3 - Q1 
        
        if pd.isna(IQR) or IQR == 0:
            continue

        upper_bound = Q3 + 1.5 * IQR 
        df[column] = df[column].clip(upper=upper_bound)

    return df 


def save_mart(df: pd.DataFrame, table_name: str) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )
