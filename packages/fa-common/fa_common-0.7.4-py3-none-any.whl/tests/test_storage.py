import os
import requests
from io import BytesIO

import pytest
from fastapi import FastAPI, UploadFile

from pathlib import Path

from fa_common import create_app, start_app, utils
from fa_common.storage import get_storage_client

from .conftest import clean_env, TEST_USER_BUCKET

dirname = os.path.dirname(__file__)
test_data_path = os.path.join(dirname, "data")


async def exercise_storage(path: str):
    bucket_name = TEST_USER_BUCKET

    app = create_app(env_path=path)
    await start_app(app)
    utils.current_app = app

    assert isinstance(app, FastAPI)
    client = get_storage_client()

    await client.make_bucket(bucket_name)
    assert await client.bucket_exists(bucket_name)

    filename = "file1.txt"
    up_file = UploadFile(
        filename=filename, file=open(os.path.join(test_data_path, filename), "rb")
    )
    # Test file upload
    file_ref = await client.upload_file(up_file, bucket_name, "files")
    assert file_ref is not None

    # Test list files
    files = await client.list_files(bucket_name, "files")
    assert files is not None and len(files) > 0

    # Test get file returns file correctly
    file_stream = await client.get_file(bucket_name, "files/file1.txt")

    with open(os.path.join(test_data_path, filename), "rb") as fin:
        test_file_bytes = BytesIO(fin.read())
        assert (
            file_stream is not None
            and file_stream.getvalue() == test_file_bytes.getvalue()
        )

    # Test file exists Negative
    file_stream2 = await client.file_exists(bucket_name, "files/file3.txt")
    assert file_stream2 is False

    # Test file exists Positive
    file_stream2 = await client.file_exists(bucket_name, "files/file1.txt")
    assert file_stream2 is True

    try:
        download_ref = await client.create_temp_file_ref(bucket_name, "files/file1.txt")

        r = requests.get(download_ref.url)  # type: ignore
        target_path = Path(os.path.join(dirname, "output", download_ref.name))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "wb") as _file:
            _file.write(r.content)
        assert os.path.exists(os.path.join(dirname, "output", download_ref.name))
    except NotImplementedError:
        pass

    # Test Copy a file
    await client.copy_file(
        bucket_name, "files/file1.txt", bucket_name, "files/file1_copy.txt"
    )
    file1_exists = await client.file_exists(bucket_name, "files/file1.txt")
    file1_copy_exists = await client.file_exists(bucket_name, "files/file1_copy.txt")
    assert file1_exists and file1_copy_exists

    # Test Rename a file
    await client.rename_file(bucket_name, "files/file1.txt", "files/file1_renamed.txt")
    file1_exists = await client.file_exists(bucket_name, "files/file1.txt")
    file1_r_exists = await client.file_exists(bucket_name, "files/file1_renamed.txt")
    assert file1_exists is False and file1_r_exists

    # Test get file returns None when file doesn't exist
    file_stream3 = await client.get_file(bucket_name, "files/file3.txt")
    assert file_stream3 is None

    filename = "file2.txt"
    up_file2 = UploadFile(
        filename=filename, file=open(os.path.join(test_data_path, filename), "rb")
    )
    file_ref = await client.upload_file(up_file2, bucket_name, "files/folder")

    assert file_ref is not None

    file_ref = await client.upload_string(
        "test_string weee", bucket_name, "files/test_string.txt"
    )
    assert file_ref is not None
    assert await client.file_exists(
        bucket_name, "files/test_string.txt"
    ), "test_string.txt Is missing from bucket"

    # Test folder exists
    assert await client.folder_exists(
        bucket_name, "files/"
    ), "Folder Is missing from bucket or testing for folders is not working"

    # Test non existing folder does not exists
    assert not await client.folder_exists(
        bucket_name, "files_not/"
    ), "Testing for non existing folder failed"

    # Test deleting a folder
    assert await client.file_exists(
        bucket_name, "files/folder/file2.txt"
    ), "File2 Is missing from bucket"
    await client.delete_file(bucket_name, "files/folder", True)
    assert not await client.file_exists(
        bucket_name, "files/folder/file2.txt"
    ), "File2 Is in bucket when it should be deleted"
    assert not await client.file_exists(
        bucket_name, "files/folder/"
    ), "Folder still exists when it should be deleted"

    await client.delete_bucket(bucket_name)
    assert not await client.bucket_exists(bucket_name)

    clean_env()


@pytest.mark.asyncio
async def test_minio_storage(minio_env_path):
    await exercise_storage(minio_env_path)


@pytest.mark.asyncio
async def test_firbase_storage(env_path):
    await exercise_storage(env_path)
