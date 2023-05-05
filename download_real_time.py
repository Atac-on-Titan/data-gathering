"""Script for downloading and saving the real time ATAC data."""

import requests
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download and save real time data from Rome Open Data.')

    parser.add_argument('-t', '--type', required=True, choices=["trip-updates", "vehicle-positions"], type=str, help="The type of data to download")
    parser.add_argument('-o', '--output', type=str, help="The directory where the files will be stored. If not specified, will store in current directory.")
    args = parser.parse_args()

    base_url = "https://dati.comune.roma.it/catalog/dataset/a7dadb4a-66ae-4eff-8ded-a102064702ba/resource"

    urls = {"trip-updates": f"{base_url}/bf7577b5-ed26-4f50-a590-38b8ed4d2827/download/rome_trip_updates.pb",
            "vehicle-positions": f"{base_url}/d2b123d6-8d2d-4dee-9792-f535df3dc166/download/rome_vehicle_positions.pb"}

    url = urls[args.type]

    response = requests.get(url)
