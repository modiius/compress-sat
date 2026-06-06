import argparse
import os
import pickle

import ee
import pandas as pd

def init_earth_engine(project: str):
    try:
        ee.Initialize(project=project)
    except ee.EEException:
        ee.Authenticate()
        ee.Initialize(project=project)


def download_dynamic_world(lat: float, lon: float, band: str, data_dir: str):
    os.makedirs(data_dir, exist_ok=True)

    point = ee.Geometry.Point([lon, lat])
    dw_collection = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").select(band).getRegion(point, scale=10)

    data = dw_collection.getInfo()
    df = ee_array_to_df(data, list_of_bands=[band])

    with open(os.path.join(data_dir, f"dw_{band}"), "wb") as f:
        pickle.dump(list(df.get(band)), f)
    

def load_dynamic_world(data_path: str):
    with open(data_path, "rb") as f:
        data = pickle.load(f)
    
    return data


def ee_array_to_df(arr, list_of_bands):
    df = pd.DataFrame(arr)

    # Rearrange the header.
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)

    # Remove rows without data inside.
    df = df[['longitude', 'latitude', 'time', *list_of_bands]].dropna()

    # Convert the data to numeric values.
    for band in list_of_bands:
        df[band] = pd.to_numeric(df[band], errors='coerce')

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Dynamic World data for a given image ID.")
    parser.add_argument("--project", type=str, help="Google Cloud project ID for Earth Engine.")
    parser.add_argument("--output_dir", type=str, default="./data", help="Directory to save the downloaded data.")
    parser.add_argument("--band", type=str, default="tree", help="Dynamic World band to download.")
    parser.add_argument("--lat", type=float, default=49.187783, help="Latitude of the point to filter Dynamic World images.")
    parser.add_argument("--lon", type=float, default=22.480810, help="Longitude of the point to filter Dynamic World images.")
    args = parser.parse_args()

    init_earth_engine(args.project)
    # download_dynamic_world(args.lat, args.lon, args.band, args.output_dir)
    data = load_dynamic_world("data/dw_trees")
    print(data)