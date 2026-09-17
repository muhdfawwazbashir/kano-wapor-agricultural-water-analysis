# Kano WaPOR Agricultural Water Analysis

## Overview

This project demonstrates the use of Python to analyze agricultural water-use indicators from the FAO WaPOR 3 dataset for Kano State, Nigeria.

The analysis focuses on 44 Local Government Areas (LGAs) in Kano State and examines:

- Actual Evapotranspiration and Interception (AETI)
- Relative Soil Moisture (RSM)

The objective is to demonstrate a reproducible geospatial workflow for downloading, processing, analyzing, and visualizing WaPOR data using Python.

## Study Area

The study area is Kano State, Nigeria, located in northern Nigeria.

The analysis was conducted at the Local Government Area (LGA) level using 44 LGAs covering Kano State.

## Data

The project uses WaPOR 3 data accessed using the `wapordl` Python package.

### AETI

- WaPOR variable: `L2-AETI-D`
- Description: Actual Evapotranspiration and Interception
- Unit: mm/day

### RSM

- WaPOR variable: `L2-RSM-D`
- Description: Relative Soil Moisture
- Unit: %

## Methodology

1. Define the Kano State study area.
2. Obtain the Kano LGA boundaries.
3. Download WaPOR 3 raster data using Python.
4. Extract zonal statistics for each LGA.
5. Calculate temporal averages.
6. Calculate annual AETI and RSM indicators.
7. Join the results to the LGA boundaries.
8. Create maps and graphs using Python.
9. Export the processed results as CSV and GeoPackage files.

## Results

### AETI

The 2024 AETI analysis produced observations for all 44 LGAs.

Annual mean AETI values ranged from approximately 289 to 858 mm/year across the LGAs.

### Relative Soil Moisture

The 2024 RSM analysis produced 36 observations for each of the 44 LGAs.

The annual mean RSM across the study area was approximately 39.6%.

The LGA-level annual mean RSM values ranged from approximately 26.3% to 53.0%.

## Outputs

The project produces:

- LGA-level AETI CSV data
- LGA-level RSM CSV data
- GeoPackage spatial data
- AETI maps
- RSM maps
- Exploratory graphs

Example output files:

- `kano_lga_aeti_2024.csv`
- `kano_lga_rsm_2024.csv`
- `kano_lga_aeti_stress_2024.gpkg`

## Technologies

- Python
- GeoPandas
- Rasterio
- NumPy
- Pandas
- Matplotlib
- Rasterstats
- WaPOR 3
- wapordl

## Author

**Muhammad Fawwaz Bashir**

Geospatial / Remote Sensing / Agricultural Water Analysis

## Data Source

FAO WaPOR 3

https://www.fao.org/in-action/remote-sensing-for-water-productivity/en/

## License

This repository contains analysis code and derived results. The underlying WaPOR data remain subject to their original terms and attribution requirements.
