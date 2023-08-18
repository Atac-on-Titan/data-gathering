"""Module for downloading all of the data that we are interested in."""
import os

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


def download_historical_weather(start: int, end: int, **kwargs):
    """Downloads hourly historical weather data using the OpenWeather API.

    :arg
        start (int): the UTC start time.
        end (int): the UTC end time.
        **kwargs: keyword arguments that should be passed to the function.

    :Keyword Args (3 mutually exclusive groups)
        lat (float): the latitude of the place for which to get the weather. Only use together with lon.
        lon (float): the longitude of the place for which to get the weather. Only use together with lat.

        id (int): the ID of the city for which to get the weather. Do not use with lat and lon.

        city (str): the name of the city for which to get the weather.
        country (str): a two letter country code.

    :return

    """
    open_weather_base_url = "https://history.openweathermap.org/data/2.5/history/city"
    api_key = os.getenv("api-key")

    if "lat" in kwargs.keys() and "lon" in kwargs.keys():
        lat, lon = kwargs.get("lat"), kwargs.get("lon")
        query_url = f"{open_weather_base_url}?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={api_key}"

    elif "id" in kwargs.keys():
        id = kwargs.get("id")
        query_url = f"{open_weather_base_url}?id={id}&type=hour&start={start}&end={end}&appid={api_key}"

    elif "country" in kwargs.keys() and "city" in kwargs.keys():
        city, country = kwargs.get("city"), kwargs.get("country")
        query_url = f"{open_weather_base_url}?q={city},{country}&type=hour&start={start}&end={end}&appid={api_key}"
    else:
        raise ValueError("Required keyword arguments not present.")

    return requests.get(query_url).content
