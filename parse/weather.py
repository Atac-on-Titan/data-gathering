"""Module for parsing weather response data."""
import pandas as pd


def parse_weather(data: dict):
    """Parses JSON weather data into a pandas dataframe.

    :arg
        data (dict): the JSON response of the weather request.

    :return
        (pd.DataFrame)
    """
    # Initialize empty lists to store data
    timestamps = []
    temps = []
    feels_like = []
    pressure = []
    humidity = []
    temp_min = []
    temp_max = []
    wind_speed = []
    wind_deg = []
    clouds = []
    weather_main = []
    weather_description = []
    weather_icon = []

    # Loop through the JSON data and extract the required fields
    for item in data["list"]:
        timestamps.append(item['dt'])
        main_data = item['main']
        temps.append(main_data['temp'])
        feels_like.append(main_data['feels_like'])
        pressure.append(main_data['pressure'])
        humidity.append(main_data['humidity'])
        temp_min.append(main_data['temp_min'])
        temp_max.append(main_data['temp_max'])
        wind_data = item['wind']
        wind_speed.append(wind_data['speed'])
        wind_deg.append(wind_data['deg'])
        clouds.append(item['clouds']['all'])
        weather_data = item['weather'][0]
        weather_main.append(weather_data['main'])
        weather_description.append(weather_data['description'])
        weather_icon.append(weather_data['icon'])

    # Create a DataFrame
    data = {
        'timestamp': timestamps,
        'temperature': temps,
        'feels_like': feels_like,
        'pressure': pressure,
        'humidity': humidity,
        'temp_min': temp_min,
        'temp_max': temp_max,
        'wind_speed': wind_speed,
        'wind_deg': wind_deg,
        'clouds': clouds,
        'weather_main': weather_main,
        'weather_description': weather_description,
        'weather_icon': weather_icon
    }

    return pd.DataFrame(data)
