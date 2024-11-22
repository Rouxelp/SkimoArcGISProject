from pydantic import BaseModel
from typing import Literal, Optional, Tuple

class BBox(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float

class MNTConfig(BaseModel):
    source: Literal["arcgis", "local"]
    local_path: Optional[str] = None  # Path is required only if source is 'local'
    bbox: BBox

class SlopeConfig(BaseModel):
    source: Literal["arcgis", "local"]
    local_path: Optional[str] = None  # Path is required only if source is 'local'
    slope_output_name: str

class HillshadeConfig(BaseModel):
    source: Literal["arcgis", "local"]
    hillshade_output_name: str
    local_path: Optional[str] = None  # Path is required only if source is 'local'

class MapConfig(BaseModel):
    center_location: Tuple[float, float]  # Latitude and Longitude
    zoom_level: int = 12  # Default zoom level

class AppConfig(BaseModel):
    # ArcGIS credentials
    username: str
    password: str

    # Nested configurations
    mnt_config: MNTConfig
    slope_config: SlopeConfig
    hillshade_config: HillshadeConfig
    map_config: MapConfig

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        """
        Create an AppConfig instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing the configuration.
        
        Returns:
            AppConfig: An AppConfig instance with nested configurations.
        """
        # Extract nested configurations and build objects



class AppConfig(BaseModel):
    # ArcGIS credentials
    username: str
    password: str

    # Nested configurations
    mnt_config: MNTConfig
    slope_config: SlopeConfig
    hillshade_config: HillshadeConfig
    map_config: MapConfig

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        """
        Create an AppConfig instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing the configuration.
        
        Returns:
            AppConfig: An AppConfig instance with nested configurations.
        """
        # Extract nested configurations and build objects
        mnt_bbox = BBox(**data["mnt_config"]["bbox"])
        mnt_config = MNTConfig(bbox=mnt_bbox, **{k: v for k, v in data["mnt_config"].items() if k != "bbox"})

        slope_config = SlopeConfig(**data["slope_config"])

        hillshade_config = HillshadeConfig(**data["hillshade_config"])
        
        map_config = MapConfig(**data["map_config"])

        # Create the AppConfig object with the nested configs
        return cls(
            username=data["username"],
            password=data["password"],
            mnt_config=mnt_config,
            slope_config=slope_config,
            hillshade_config=hillshade_config,
            map_config=map_config,
        )
