from pathlib import Path

from arcgis import GIS
from schemas import AppConfig
from utils.visualization import visualize_map
from utils.transfo import calculate_or_fetch_layer
from utils.loader import load_config_from_yaml, load_mnt
from utils.logger import handle_logger

logger = handle_logger()

def main(config: AppConfig) -> None:
    """
    Main function to execute the workflow.
    
    Args:
        config (AppConfig): Centralized application configuration.
    """
    logger.info("Starting workflow with arcpy...")

    # GIS connection 
    gis = GIS("https://www.arcgis.com", config.username, config.password)
    logger.info(f"Connected as: {gis.properties.user.username}")

    # Load or retrieve MNT
    mnt_path = load_mnt(config, gis)

    # Slope layer: calculate or fetch
    slope_path = Path(f"{config.slope_config.local_path}{config.slope_config.slope_output_name}.tif")
    slope_layer = calculate_or_fetch_layer(
        layer_type="slope", 
        mnt_path=mnt_path, 
        output_path=slope_path
    )

    # Hillshade layer: calculate or fetch
    hillshade_path = Path(f"{config.hillshade_config.local_path}{config.hillshade_config.hillshade_output_name}.tif")
    hillshade_layer = calculate_or_fetch_layer(
        layer_type="hillshade", 
        mnt_path=mnt_path, 
        output_path=hillshade_path
    )

    # Visualize results
    map_view = visualize_map(
        gis,
        [slope_layer, hillshade_layer], 
        config=config
    )
    logger.info("Workflow completed. Map view is ready. Displaying...")

    logger.info(f"Map view URL: {map_view}")
    map_view


if __name__ == "__main__":
    config = load_config_from_yaml()
    main(config)
