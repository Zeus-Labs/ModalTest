import os
import shutil
import subprocess
import zipfile

from loguru import logger


class DownloadError(Exception):
    pass


def download_file(url, destination_folder, file_name):
    # file_name = get_file_name(url)
    file_path = os.path.join(destination_folder, file_name)

    if os.path.exists(file_path):
        logger.debug(f"{file_name} already exists. Skipping download.")
        return file_path

    try:
        # Use gdown to download the file
        result = subprocess.run(['gdown', url],
                                cwd=destination_folder,
                                check=True,
                                capture_output=True,
                                text=True)

        if "Access denied" in result.stderr:
            raise DownloadError("Access denied. The file might not be publicly accessible.")

        logger.debug(f"Successfully downloaded {file_name}")
        return file_path

    except subprocess.CalledProcessError as e:
        raise DownloadError(f"Failed to download {file_name}: {e.stderr}")


def unzip_file(zip_path, extract_to, file_name):
    file_path = os.path.join(extract_to, file_name)
    if os.path.exists(file_path):
        logger.debug(f"{file_name} already exists. Skipping unzipping the file.")
        return file_path

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    logger.debug(f"Extracted {zip_path} to {extract_to}")
    return file_path


def copy_files(source_dir, destination_dir, file_names=[]):
    """
    Copy mulitple file from source to destination.
    """
    for file_name in file_names:
        source_file_path = os.path.join(source_dir, file_name)
        copy_file(source_file_path, destination_dir)


def copy_file(source, destination):
    """
    Copy a file from source to destination.
    """
    try:
        shutil.copy2(source, destination)
        logger.debug(f"File copied: {source} -> {destination}")
    except FileNotFoundError:
        logger.debug(f"Source file not found: {source}")
    except PermissionError:
        logger.debug(f"Permission denied: Unable to copy {source}")


def copy_directory(source, destination):
    """
    Copy an entire directory and its contents.
    """
    try:
        shutil.copytree(source, destination)
        logger.debug(f"Directory copied: {source} -> {destination}")
    except FileExistsError:
        logger.debug(f"Destination directory already exists: {destination}")
    except FileNotFoundError:
        logger.debug(f"Source directory not found: {source}")
