"""
Kano WaPOR Agricultural Water Analysis
Author: Muhammad Fawwaz Bashir

Analysis of AETI and Relative Soil Moisture (RSM) for
44 Local Government Areas in Kano State, Nigeria.

Data source:
FAO WaPOR 3

Main variables:
- L2-AETI-D: Actual Evapotranspiration and Interception
- L2-RSM-D: Relative Soil Moisture
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

from rasterstats import zonal_stats
from wapordl import wapor_dl


# ============================================================
# 1. Project paths
# ============================================================

OUTPUT_DIR = "outputs"
DATA_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. Study area
# ============================================================

KANO_LGA = "data/raw/kano_lgas_stress_2024.geojson"

lgas = gpd.read_file(KANO_LGA)

print("Number of LGAs:", len(lgas))
print(lgas["LGA"].head())


# ============================================================
# 3. AETI analysis
# ============================================================

AETI_RASTER = "data/raw/bb_L2-AETI-D_NONE_none.tif"

# The WaPOR raster contains 37 dekadal bands.
# Zonal statistics can be calculated for each band.

with rasterio.open(AETI_RASTER) as src:

    print("AETI raster:")
    print("Width:", src.width)
    print("Height:", src.height)
    print("Bands:", src.count)
    print("CRS:", src.crs)

    aeti_results = []

    for band in range(1, src.count + 1):

        raster = src.read(band)

        stats = zonal_stats(
            lgas,
            raster,
            affine=src.transform,
            nodata=src.nodata,
            stats=["mean"],
        )

        date = src.descriptions[band - 1]

        for lga_name, stat in zip(lgas["LGA"], stats):

            aeti_results.append({
                "LGA": lga_name,
                "date": date,
                "AETI_mm_day": stat["mean"] * 0.1
                if stat["mean"] is not None else np.nan
            })


aeti_lga = pd.DataFrame(aeti_results)

aeti_lga["date"] = pd.to_datetime(aeti_lga["date"])

aeti_annual = (
    aeti_lga
    .groupby("LGA", as_index=False)["AETI_mm_day"]
    .mean()
)

aeti_annual["Annual_AETI_mm"] = (
    aeti_annual["AETI_mm_day"] * 365
)

aeti_annual = aeti_annual.drop(columns=["AETI_mm_day"])


# ============================================================
# 4. Relative Soil Moisture analysis
# ============================================================

RSM_RASTER = "data/raw/bb_L2-RSM-D_NONE_none.tif"

with rasterio.open(RSM_RASTER) as src:

    rsm_results = []

    for band in range(1, src.count + 1):

        raster = src.read(band)

        stats = zonal_stats(
            lgas,
            raster,
            affine=src.transform,
            nodata=src.nodata,
            stats=["mean"],
        )

        date = src.descriptions[band - 1]

        for lga_name, stat in zip(lgas["LGA"], stats):

            rsm_results.append({
                "LGA": lga_name,
                "date": date,
                "RSM_percent": stat["mean"] * 0.1
                if stat["mean"] is not None else np.nan
            })


rsm_lga = pd.DataFrame(rsm_results)

rsm_lga["date"] = pd.to_datetime(rsm_lga["date"])


rsm_annual = (
    rsm_lga
    .groupby("LGA", as_index=False)["RSM_percent"]
    .mean()
    .rename(columns={
        "RSM_percent": "Annual_mean_RSM_percent"
    })
)


# ============================================================
# 5. Join results to LGA boundaries
# ============================================================

results = lgas.merge(
    aeti_annual,
    on="LGA",
    how="left"
)

results = results.merge(
    rsm_annual,
    on="LGA",
    how="left"
)


# ============================================================
# 6. Export results
# ============================================================

results.to_file(
    "data/processed/kano_wapor_results.gpkg",
    driver="GPKG"
)

aeti_lga.to_csv(
    "data/processed/kano_lga_aeti_2024.csv",
    index=False
)

aeti_annual.to_csv(
    "data/processed/kano_lga_annual_aeti_2024.csv",
    index=False
)

rsm_lga.to_csv(
    "data/processed/kano_lga_rsm_2024.csv",
    index=False
)

rsm_annual.to_csv(
    "data/processed/kano_lga_annual_rsm_2024.csv",
    index=False
)


print("\nAnalysis complete.")
print("AETI observations:", len(aeti_lga))
print("RSM observations:", len(rsm_lga))
print("LGAs:", len(results))
