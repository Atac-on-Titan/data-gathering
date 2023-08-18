"""Script for downloading historical weather data."""
import argparse
import logging
from datetime import datetime
from pathlib import Path

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

    logger.info(f"Fetching historical weather data for timeframe: {args.start} - {args.end}")
    weather_resp = download_historical_weather(args.start, args.end, city="ROMA", country="IT")

    logger.info(f"Parsing downloaded weather data.")
    weather_df = parse_weather(weather_resp)

    output_path = f"{args.output}/weather_df.feather"

    logger.info(f"Saving weather data to {output_path}")
    weather_df.to_feather(output_path)
