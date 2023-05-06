"""Module for downloading all of the data that we are interested in."""

import requests

base_url = "https://dati.comune.roma.it/catalog/dataset/a7dadb4a-66ae-4eff-8ded-a102064702ba/resource"
trip_updates_url = f"{base_url}/bf7577b5-ed26-4f50-a590-38b8ed4d2827/download/rome_trip_updates.pb"
vehicle_positions_url = f"{base_url}/d2b123d6-8d2d-4dee-9792-f535df3dc166/download/rome_vehicle_positions.pb"


def download_trip_updates():
    """Downloads the ATAC trip updates.

    :returns
        The binary response content.
    """
    return requests.get(trip_updates_url).content


def download_vehicle_positions():
    """Downloads the ATAC vehicle positions.

    :returns
        The binary response content.
    """
    return requests.get(vehicle_positions_url).content
