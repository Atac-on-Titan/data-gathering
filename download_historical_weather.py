"""Script for downloading historical weather data."""
import argparse
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from download import download_historical_weather
from parse import parse_weather

if __name__ == "__main__":
    log_dir = "logs"
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(filename=f'{log_dir}/{current_date}_app.log', filemode='a', format='%(name)s:%(levelname)s:%(asctime)s - %(message)s')
    logger = logging.getLogger("download_real_time")
    logger.setLevel(logging.INFO)

    # load environment variables
    load_dotenv()

    # Create an argument parser with arguments
    parser = argparse.ArgumentParser(description='Download hourly historical weather data and save into a dataframe.')
    parser.add_argument('-s', '--start', required=True, type=int, help="The UTC start time.")
    parser.add_argument('-e', '--end', required=True, type=int, help="The UTC end time.")
    parser.add_argument('-o', '--output', required=True, type=str, help="The output directory.")

    # Parse the arguments
    args = parser.parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)

    start_unix = args.start
    end_unix = args.end

    from datetime import datetime

    # Convert Unix timestamps to datetime objects
    start = datetime.utcfromtimestamp(start_unix)
    end = datetime.utcfromtimestamp(end_unix)

    # Calculate the time difference
    time_difference = end - start

    week_seconds = 7 * 24 * 60 * 60

    query_start = start_unix
    query_end = start_unix + week_seconds

    weather_dfs = []

    if time_difference.days > 6:
        while query_end < args.end:
            logger.info(f"Fetching historical weather data for timeframe: {query_start} - {query_end}")
            weather_resp = download_historical_weather(query_start, query_end, city="ROMA", country="IT")

            logger.info(f"Parsing downloaded weather data.")
            weather_dfs.append(parse_weather(weather_resp))

            query_start = query_end
            query_end += week_seconds

    weather_df = pd.concat(weather_dfs, ignore_index=True)

    output_path = f"{args.output}/weather_df.feather"

    logger.info(f"Saving weather data to {output_path}")
    weather_df.to_feather(output_path)
