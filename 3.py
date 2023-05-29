#AGEENCOVA

import os
import shapefile
import json
import csv
import sys
import requests
import zipfile
from tqdm import tqdm

def downloadCoastline():
    # URL for downloading
    url = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_coastline.zip"

    # folder for saving
    folder = "coastline"

    # create folder if it didnt exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        # clear folder if it exists
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Downloading file
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 KB
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    with open(os.path.join(folder, "ne_10m_coastline.zip"), "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    print("Unzipping archive")
    # unzip file
    zip_path = os.path.join(folder, "ne_10m_coastline.zip")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(folder)

    # delete zip archive after unzip
    os.remove(zip_path)

def shp_to_json(input_shp, output_json):
    reader = shapefile.Reader(input_shp)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    data = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        data.append({"properties": atr, "geometry": geom})

    with open(output_json, 'w') as json_file:
        json.dump(data, json_file)

    print(f"Converted: {input_shp}")


def json_to_csv(input_json, output_csv):
    with open(input_json, 'r') as json_file:
        data = json.load(json_file)

    with open(output_csv, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write CSV header
        header = ["latitude", "longitude"]
        writer.writerow(header)

        # Write data rows
        for item in data:
            coordinates = item["geometry"]["coordinates"]
            for coord in coordinates:
                writer.writerow([coord[1], coord[0]])


downloadCoastline()

# Input folder containing SHP files, output folder for JSON and CSV files
input_folder = "coastline"
output_folder = "coastline/output_convert"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all SHP files in the input folder
shp_files = [file for file in os.listdir(input_folder) if file.lower().endswith(".shp")]

total_files = len(shp_files)
processed_files = 0

# Iterate through each SHP file and perform the conversion
for shp_file in shp_files:
    processed_files += 1
    print(f"Converting in file {processed_files}/{total_files}: {shp_file}")

    # Construct the file paths for input and output files
    input_shp = os.path.join(input_folder, shp_file)
    output_json = os.path.join(output_folder, f"{os.path.splitext(shp_file)[0]}.json")
    output_csv = os.path.join(output_folder, f"{os.path.splitext(shp_file)[0]}.csv")

    # Perform the conversion
    shp_to_json(input_shp, output_json)
    json_to_csv(output_json, output_csv)

print("Converting successfully done")