import os

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from ..schemas.s3_schema import S3ResponseModel
from ..utils.exception import InvalidDestination, InvalidFileType
from ..utils.handle_file import save_to_FS, validate_file_type
from ..utils.s3_client import download_convert_file, download_file, upload_file

router = APIRouter()
# Serve static files
router.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        + "/static"
    ),
    name="static",
)


@router.post("/upload_s3/", response_model=S3ResponseModel)
async def upload_s3(
    bucket_name: str,
    path: str,
    type: str,
    user_id: str,
    file_id: str,
    file: UploadFile = File(...),
):
    """Upload the file to s3 by binaries"""
    # Get the extension of file
    extension = validate_file_type(file, type)
    if not extension:
        raise InvalidFileType(detail=f"Your upload file must be a {type}")

    res = await upload_file(
        file.file,
        bucket_name,
        path,
        type,
        user_id,
        file_id + f".{extension}",
    )
    if not res["status"]:
        raise InvalidDestination(detail=res["message"])
    return res


@router.get("/download_s3/", response_model=S3ResponseModel)
async def download_s3(bucket_name: str, path: str, task_id: str):
    """Download the file with bucket name and key from s3, save in static/generation"""
    res = await download_file(bucket_name, path)
    if not res["status"]:
        raise InvalidDestination(detail=res["message"])
    save_to_FS("generation", task_id, "mp4", res["file_content"])
    return {
        "bucket_name": bucket_name,
        "path": path,
        "file_name": f"{task_id}.mp4",
    }


@router.get("/get_binary/")
async def get_binary(bucket_name: str, path: str, type: str):
    res = await download_file(bucket_name, path)
    return Response((res["file_content"]), media_type=f"{type}/*")


@router.get("/get_binary_video_convert_codecs/")
async def get_binary_video_convert_codecs(bucket_name: str, path: str, type: str):
    res = await download_convert_file(bucket_name, path)
    return Response((res["file_content"]), media_type=f"{type}/*")
