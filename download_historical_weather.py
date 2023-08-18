"""Script for downloading historical weather data."""
import argparse
import logging
from datetime import datetime
from pathlib import Path
from download import download_historical_weather
from dotenv import load_dotenv

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

    download_historical_weather(args.start, args.end, city="ROMA", country="IT")

