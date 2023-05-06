"""Script for downloading and saving the real time ATAC data."""

import argparse
import logging
from datetime import datetime
from pathlib import Path

from download import download_trip_updates, download_vehicle_positions

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode='a', format='%(name)s:%(levelname)s:%(asctime)s - %(message)s')
    logger = logging.getLogger("download_real_time")
    logger.setLevel(logging.INFO)

    # Create an argument parser with arguments
    parser = argparse.ArgumentParser(description='Download and save real time data from Rome Open Data.')
    parser.add_argument('-t', '--type', required=True, choices=["trip-updates", "vehicle-positions"], type=str,
                        help="The type of data to download")
    parser.add_argument('-o', '--output', type=str,
                        help="The directory where the files will be stored. If not specified, will store in current "
                             "directory.")

    # Parse the arguments
    args = parser.parse_args()

    download = {"trip-updates": download_trip_updates, "vehicle-positions": download_vehicle_positions}

    # Extract the arguments
    download = download[args.type]
    out_dir = args.output if args.output else "./"

    logger.info(f"Parsed arguments: type = {args.type}; output = {out_dir}")

    # Create output path and make its directory if it doesn't exist
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = f"{out_dir}rome-{args.type}_{current_datetime}.pb"
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    logger.info(f"Fetching {args.type} file.")

    downloaded_data = download()

    logger.info(f"Writing into {out_path}")
    with open(out_path, mode='wb') as outfile:
        outfile.write(downloaded_data)
