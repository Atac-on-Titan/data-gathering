import argparse
import glob
import logging
import os.path
from pathlib import Path

import pandas as pd
from google.protobuf.message import DecodeError
from google.transit import gtfs_realtime_pb2
from tqdm import tqdm

def add_missing_slash(path):
    if path[-1] in ["/", "\\"]:
        return path

    return f"{path}/"


def save_trip_updates(stop_updates, path):
    """Saves a list of stop updates to the provided path.

    The stop updates are appended to an existing dataframe if it exists.

    :arg
        stop_updates: a list of lists.
        path (str): the path where to save the stop updates.
    """
    logger.info("Creating dataframe.")
    trip_updates = pd.DataFrame(stop_updates, columns=columns)

    if os.path.exists(path):
        existing_df = pd.read_feather(path)
        trip_updates = pd.concat((existing_df, trip_updates), ignore_index=True, axis=0)

    logger.info(f"Saving dataframe at {path}")
    trip_updates.to_feather(path)


if __name__ == '__main__':
    log_dir = "logs"
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logging.basicConfig(format='%(name)s:%(levelname)s:%(asctime)s - %(message)s', handlers=[
        logging.FileHandler("logs/debug.log", mode='a'),
        logging.StreamHandler()
    ])
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Reading files')

    parser.add_argument('-i', '--in-path', type=str, required=True, help="Path to directory of .pb files.")
    parser.add_argument('-o', '--out-dir', type=str, required=True, help="Output directory where the parsed data will be saved.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose flag, will print out a tqdm loop.")
    args = parser.parse_args()

    # add a slash to the provided path if it is missing
    in_path = add_missing_slash(args.in_path)
    out_dir = add_missing_slash(args.out_dir)
    out_path = f"{out_dir}trip-updates.feather"

    files = glob.glob(f"{in_path}*.pb")
    logger.info(f"Found {len(files)} .pb files to read.")

    columns = ["trip_id", "start_time", "start_date", "route_id", "stop_sequence", "delay", "time", "uncertainty", "stop_id"]
    stop_updates = []

    for i, file in tqdm(enumerate(files), disable=not args.verbose):
        with open(file, 'rb') as f:

            feed = gtfs_realtime_pb2.FeedMessage()

            try:
                feed.ParseFromString(f.read())
            except DecodeError as de:
                logger.warning(f"Could not parse {file}. {de}")

            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    trip = entity.trip_update.trip
                    trip_id = trip.trip_id
                    start_time = trip.start_time
                    start_date = trip.start_date
                    route_id = trip.route_id

                    for stop_time_update in entity.trip_update.stop_time_update:
                        stop_sequence = stop_time_update.stop_sequence
                        delay = stop_time_update.arrival.delay
                        time = stop_time_update.arrival.time
                        uncertainty = stop_time_update.arrival.uncertainty
                        stop_id = stop_time_update.stop_id

                        stop_update = [trip_id, start_time, start_date, route_id, stop_sequence, delay, time, uncertainty, stop_id]

                        stop_updates.append(stop_update)

        if i % 100 == 0 and i > 0:
            save_trip_updates(stop_updates, out_path)
            stop_updates = []

    logger.info("Finished reading all files.")
    save_trip_updates(stop_updates, out_path)
