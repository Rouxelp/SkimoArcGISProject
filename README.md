# **Ski Tour Avalanche Risk Analysis**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![ArcGIS](https://img.shields.io/badge/ArcGIS-Online%20%26%20Pro-orange)](https://www.esri.com/en-us/arcgis/products/arcgis-online/overview)

## **Overview**
This project leverages **GIS tools**, **machine learning**, and **thermodynamic modeling** to predict and analyze avalanche risks for **ski touring** in mountainous regions like Chamonix. By combining slope analysis, meteorological data, and historical avalanche occurrences, it delivers an **interactive map** that visualizes high-risk zones and assists skiers in making safer decisions.

---

## **Features**
- **Slope Analysis**: Extracts slope information from Digital Elevation Models (DEM) to highlight critical areas with steep inclines.
- **Hillshade Visualization**: Creates shaded relief maps for better visualization of terrain features.
- **Thermodynamic Snow Model**: Simulates snow behavior using a basic thermodynamic model to evaluate snow melting, freezing, and compositional changes.
- **Machine Learning Model**: Trains a neural network on historical avalanche data and weather conditions to predict avalanche risks.
- **Interactive Map**: Publishes layers (slope, hillshade, and predicted risk zones) to **ArcGIS Online**, allowing real-time visualization of avalanche risks.
- **GPX Compatibility**: Supports GPX file import for route planning and risk assessment.

---

## **Methodology**
1. **Data Preparation**:
   - Import Digital Elevation Models (DEM) for the region of interest.
   - Process meteorological data, including temperature, snowfall, and wind speed.
2. **Layer Generation**:
   - Calculate slope and hillshade layers from DEM using `arcpy`.
   - Store processed layers on **ArcGIS Online** for visualization.
3. **Avalanche Prediction**:
   - Simulate snowpack dynamics using a basic thermodynamic model.
   - Train a neural network on historical avalanche data and weather patterns.
4. **Visualization**:
   - Combine generated layers and predictions into an **ArcGIS Web Map**.
   - Share the interactive map with stakeholders via ArcGIS Online.

---

## **Requirements**
- **Python**: 3.9+
- **ArcGIS Pro** with `arcpy` installed.
- **ArcGIS Online** account for managing and publishing layers.
- Additional Python libraries:
  - `numpy`
  - `pandas`
  - `python-dotenv`
  - `torch` 
  - `scikit-learn`
  - `matplotlib`

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ski-tour-avalanche-risk.git
   cd ski-tour-avalanche-risk

2. Set up a Python virtual environment and install dependencies:
   ```bash
   python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt

3. Configure your arcgis credentials on .env file
   ```bash
   ARCGIS_USERNAME=your_username
   ARCGIS_PASSWORD=your_password

## **Utilization**

Before running the application, modify the `config.yaml` file to customize the behavior of the script, including:
- The **location** for Digital Elevation Models (DEM).
- **Output directories** for slope and hillshade layers.
- ArcGIS Online **credentials** (username and password).

Run the main script to process DEM, generate layers, and publish them to ArcGIS Online:
```bash
python main.py

```
Access the interactive map via the URL provided in the script output.

## **Project Structure**
```bash
ski-tour-avalanche-risk/
│
├── data/                         # Input and output data
│   ├── mnt/                      # Digital Elevation Models
│   ├── slope/                    # Slope layers
│   └── hillshade/                # Hillshade layers
│
├── utils/                        # Utility scripts
│   ├── loader.py                 # Load and preprocess DEM data
│   ├── transfo.py                # Generate slope and hillshade layers
│   ├── visualization.py          # Create and publish Web Maps
│   └── logger.py                 # Logging setup
│
├── models/                       # Machine learning models for avalanche prediction
│
├── schemas/                      # Configuration and data schemas
│
├── tests/                        # Unit and integration tests
│   ├── test_loader.py            # Unit tests for loader module
│   ├── test_transfo.py           # Unit tests for transformation module
│   ├── test_visualization.py     # Unit tests for visualization module
│   └── integration/              # Integration tests
│       ├── test_full_pipeline.py # Test the entire workflow
│
├── config.yaml                   # Application configuration
├── main.py                       # Main script
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation

