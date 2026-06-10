from common.connections import s3_client, settings
from common.ETL import extract_df_from_db, load_df_to_s3, load_partitioned_df_to_s3, extract_csv_from_s3, transforms_null_values, transforms_outliers


def create_bucket(s3_client, bucket_name: str) -> dict[str, str]:
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return {"ok": "Бакет существует"}
    except:
        s3_client.create_bucket(Bucket=bucket_name)
        return {"ok": "Бакет создан"}


def pipeline(table_name: str, date_column: str = None):

    create_bucket(
        s3_client=s3_client,
        bucket_name=settings.BUCKET_NAME
    )

    df = extract_df_from_db(table_name)

    if not date_column:
        load_df_to_s3(
            df=df, 
            filename=table_name, 
            prefix="raw"
        )
    else:
        load_partitioned_df_to_s3(
            df=df, 
            table_name=table_name, 
            prefix="raw", 
            date_column=date_column
        )

    df = extract_csv_from_s3(table_name=table_name, prefix="raw")

    df = transforms_null_values(df=df)

    df = transforms_outliers(df=df)

    return df
