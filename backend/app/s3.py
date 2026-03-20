import boto3
from app.config import settings


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )


def upload_to_s3(file_bytes: bytes, filename: str) -> None:
    client = get_s3_client()
    client.put_object(
        Bucket=settings.s3_bucket_name,
        Key=f"documents/{filename}",
        Body=file_bytes,
    )


def download_from_s3(filename: str) -> bytes:
    client = get_s3_client()
    response = client.get_object(
        Bucket=settings.s3_bucket_name,
        Key=f"documents/{filename}",
    )
    return response["Body"].read()


def list_s3_documents() -> list[dict]:
    client = get_s3_client()
    response = client.list_objects_v2(
        Bucket=settings.s3_bucket_name,
        Prefix="documents/",
    )
    documents = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key == "documents/":
            continue
        documents.append({
            "name": key.removeprefix("documents/"),
            "size": obj["Size"],
            "last_modified": obj["LastModified"].isoformat(),
        })
    return documents
