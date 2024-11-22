from arcgis import GIS
import yaml
from pathlib import Path
from schemas import AppConfig
from utils.utils import download_raster, get_arcgis_credentials
from utils.logger import handle_logger

logger = handle_logger()

def load_config_from_yaml(file_path: str = "config.yaml", include_credentials=True) -> AppConfig:
    """
    Load configuration from a YAML file and return a validated AppConfig object.
    
    Args:
        file_path (str): Path to the YAML configuration file.
        include_credentials (bool): Whether to include credentials in the loaded config.
    
    Returns:
        AppConfig: Validated configuration object.
    """
    # Check if the file exists
    config_path = Path(file_path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    # Load the YAML file
    with open(config_path, "r", encoding="utf-8-sig") as file:
        config_data = yaml.safe_load(file)
    
    # If include_credentials is True, add credentials to the config
    if include_credentials:
        username, password = get_arcgis_credentials()
        config_data['username'] = username
        config_data['password'] = password

    # Validate and return the config as AppConfig
    return AppConfig.from_dict(config_data)


def load_mnt(config: AppConfig, gis: GIS) -> str:
    """
    Load a Digital Elevation Model (DEM) from a local file or retrieve it from ArcGIS Online.
    
    Args:
        config (AppConfig): Configuration for MNT source.
        gis (GIS): ArcGIS connection object.
    
    Returns:
        str: Path to the MNT raster file.
    """
    if config.mnt_config.local_path is not None:
        local_mnt_path = Path(config.mnt_config.local_path)
    else:
        if config.mnt_config.source == "local":
            raise ValueError("MNT source configuration is missing or invalid. Local path is required if source is 'local'.")

    # Case 1: MNT exists locally
    if local_mnt_path.is_file():
        logger.info(f"Loading local DEM from: {local_mnt_path}")
        return str(local_mnt_path)

    # Case 2: Retrieve MNT from ArcGIS Online
    logger.info("Local DEM not found. Retrieving DEM from ArcGIS Online...")
    mnt_item = gis.content.search("Terrain Elevation", "Imagery Layer", outside_org=True)[0]
    mnt_layer = mnt_item.layers[0]
    logger.info(f"DEM retrieved from ArcGIS: {mnt_item.title}")

    # Export the MNT to a local file
    local_mnt_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

    # Perform export_image operation
    export_result = mnt_layer.export_image(
        bbox={
             "xmin": config.mnt_config.bbox.xmin,
             "ymin": config.mnt_config.bbox.ymin,
             "xmax": config.mnt_config.bbox.xmax,
             "ymax": config.mnt_config.bbox.ymax
        },
        export_format="tiff"
    )

    if "href" in export_result:
        download_url = export_result["href"]
        logger.info(f"Downloading DEM from: {download_url}")
        local_file = local_mnt_path
        download_raster(download_url, local_file)
        logger.info(f"DEM saved locally at: {local_file}")
        return str(local_file)
    else:
        raise RuntimeError("Failed to export DEM from ArcGIS Online.")


