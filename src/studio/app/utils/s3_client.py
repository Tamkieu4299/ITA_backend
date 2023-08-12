# from fastapi.responses import FileResponse
from boto3 import client

from ..constants.config import settings
from ..utils.handle_file import convert_file

# Configuration Details
ACCESS_KEY = settings.ACCESS_KEY
SECRET_KEY = settings.SECRET_KEY


# Connecting to S3
s3_client = client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


async def download_file(bucket_name: str, key: str):
    """Downloading the file as byte stream"""
    try:
        file_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    except Exception:
        return {"message": "Invalid bucket name or path", "status": False}
    file_content = file_object["Body"].read()
    return {"file_content": file_content, "status": True}


async def download_convert_file(bucket_name: str, key: str):
    """Downloading and convert the codecs of the file as byte stream"""
    try:
        file_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    except Exception:
        return {"message": "Invalid bucket name or path", "status": False}
    file_content = file_object["Body"].read()
    # Convert the file content using FFmpeg
    conversion_result = convert_file(file_content)
    if conversion_result["status"]:
        # Return the converted file data
        return {"file_content": conversion_result["file_data"], "status": True}

    return {"file_content": None, "status": False}


async def upload_file(
    file, bucket_name: str, path: str, type: str, user_id: str, file_name: str
):
    """Uploading the file as byte stream"""
    key = f"{path}/{type}/{user_id}/{file_name}"
    try:
        s3_client.upload_fileobj(file, bucket_name, key)
        return {"bucket_name": bucket_name, "path": key, "status": True}
    except Exception:
        return {
            "message": f"Invalid bucket name {bucket_name} or path {key}",
            "status": False,
        }
