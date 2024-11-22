import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Tuple
import requests

load_dotenv()

def get_arcgis_credentials() -> Tuple[str, str]:
    return os.getenv("ARCGIS_USERNAME"), os.getenv("ARCGIS_PASSWORD")

def download_raster(url: str, output_path: Path):
    """
    Download a raster file from a given URL and save it locally.

    Args:
        url (str): URL of the raster file to download.
        output_path (Path): Path to save the downloaded file.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise RuntimeError(f"Failed to download file from {url}. HTTP status code: {response.status_code}")
