from pathlib import Path
from arcgis.gis import GIS
from arcgis.raster import ImageryLayer
from typing import List
from schemas import AppConfig
from utils.logger import handle_logger

logger = handle_logger()

def visualize_map(gis: GIS, layers: List[str], config: AppConfig) -> str:
    """
    Visualize raster layers using ArcGIS Online (interactive map).
    
    Args:
        gis (GIS): GIS connection object.
        layers (List[str]): List of file paths to raster layers to visualize.
        config (AppConfig): Configuration for map visualization.
    
    Returns:
        str: URL of the created WebMap.
    """
    logger.info("Creating interactive map using ArcGIS Online...")

    # Stock televersed layers
    operational_layers = []

    for layer_path in layers:
        layer_name = Path(layer_path).stem

        # Check if element exist
        query = f"title:\"{layer_name}\" AND type:\"Image Service\" OR type:\"Layer\""
        existing_items = gis.content.search(query=query, max_items=1)

        if existing_items:
            logger.info(f"Layer '{layer_name}' already exists. Using existing item.")
            imagery_layer = ImageryLayer(existing_items[0].url)
            operational_layers.append({
                "url": imagery_layer.url,
                "visibility": True,
                "title": layer_name
            })
            continue

        try:
            # Step 1 : Add the file as a "FIle"
            layer_item = gis.content.add(
                item_properties={
                    "type": "File",
                    "title": layer_name,
                    "tags": ["Ski", "Avalanche", "Risk"],
                    "description": f"Raster layer for {layer_name}",
                },
                data=layer_path
            )
            try:
                # Analysez les paramètres de publication
                publish_parameters = layer_item.analyze()
                logger.info(f"Publish parameters for '{layer_name}': {publish_parameters}")

                # Publiez en tant qu'Imagery Layer
                published_item = layer_item.publish(
                    publish_parameters=publish_parameters, overwrite=True
                )
                logger.info(f"Published layer '{layer_name}' as Imagery Layer: {published_item.title}")
            except Exception as e:
                logger.error(f"Failed to publish layer '{layer_name}': {e}")
                raise


            # Step 2 : Publish as an Imagery Layer
            imagery_layer = ImageryLayer(published_item.url)
            operational_layers.append({
                "url": imagery_layer.url,
                "visibility": True,
                "title": layer_name,
                "layerType": "ArcGISImageServiceLayer"
            })

            logger.info(f"Uploaded and published layer '{layer_name}' as Imagery Layer.")
        except Exception as e:
            logger.error(f"Failed to upload or publish layer '{layer_path}': {e}")
            continue

    # WebMap creation
    try:
        logger.info("Creating WebMap...")
        webmap_properties = {
            "type": "Web Map",
            "title": "Ski Tour Avalanche Risk Map",
            "tags": ["Ski", "Avalanche", "Risk"],
            "snippet": "Map showing avalanche risks for ski touring in the Chamonix area.",
            "description": "A WebMap displaying slope and hillshade layers for avalanche risk analysis.",
            "text": {
                "operationalLayers": operational_layers,
                "baseMap": {
                    "baseMapLayers": [{
                        "url": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
                        "id": "basemap",
                        "title": "World Imagery",
                        "layerType": "ArcGISTiledMapServiceLayer"
                    }],
                    "title": "Base Map"
                }
            }
        }

        webmap_item = gis.content.add(item_properties=webmap_properties)
        logger.info(f"WebMap '{webmap_item.title}' created successfully.")
        return webmap_item.homepage
    except Exception as e:
        logger.error(f"Failed to create WebMap: {e}")
        return None
