import arcpy
from arcpy.sa import Slope, Hillshade
from pathlib import Path
from utils.logger import handle_logger

# Activate Spatial Analysis Extension
arcpy.CheckOutExtension("Spatial")

logger = handle_logger()

def calculate_layer(layer_type: str, mnt_path: str, output_path: str) -> str:
    """
    Perform a raster calculation (slope or hillshade) locally using arcpy.

    Args:
        layer_type (str): The type of layer to calculate ("slope" or "hillshade").
        mnt_path (str): Path to the input DEM raster file.
        output_path (str): Path to save the calculated raster.

    Returns:
        str: Path to the resulting raster file.
    """
    # Path object is not supported for arcpy
    mnt_path = str(mnt_path)
    output_path = str(output_path)

    logger.info(f"Calculating {layer_type} layer using arcpy...")

    # Perform the requested calculation
    if layer_type == "slope":
        calculated_layer = Slope(mnt_path, output_measurement="DEGREE")
    elif layer_type == "hillshade":
        calculated_layer = Hillshade(mnt_path, azimuth=315, altitude=45)
    else:
        raise ValueError("Invalid layer_type. Must be 'slope' or 'hillshade'.")

    # Save the calculated layer
    logger.info(f"Saving {layer_type} layer to {output_path}...")
    calculated_layer.save(output_path)
    logger.info(f"{layer_type.capitalize()} layer saved to {output_path}.")
    
    return output_path


def calculate_or_fetch_layer(layer_type: str, mnt_path: str, output_path: str) -> str:
    """
    Check if a precalculated layer exists. If not, perform a new calculation locally.

    Args:
        layer_type (str): The type of layer to calculate ("slope" or "hillshade").
        mnt_path (str): Path to the input DEM raster file.
        output_path (str): Path to check for the precalculated layer or save a new one.

    Returns:
        str: Path to the raster file (either fetched or newly calculated).
    """
    local_file = Path(output_path)

    if local_file.is_file():
        logger.info(f"{layer_type.capitalize()} layer already exists at {output_path}.")
        return str(local_file)

    logger.info(f"{layer_type.capitalize()} layer not found. Calculating...")
    return calculate_layer(layer_type, mnt_path, output_path)


def save_layer(layer_path: str, output_path: str) -> None:
    """
    Save a raster layer to a specified local path.

    Args:
        layer_path (str): Path to the input raster layer.
        output_path (str): Path to save the raster file locally.
    """
    logger.info(f"Saving layer to {output_path}...")
    
    # Copy the raster to the desired location
    arcpy.management.CopyRaster(layer_path, output_path)
    logger.info(f"Layer saved to {output_path}.")
