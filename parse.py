import argparse
import dataclasses
import glob
import logging.config
import os.path
from pathlib import Path

import pandas as pd
from google.protobuf.message import DecodeError
from google.transit import gtfs_realtime_pb2
from tqdm import tqdm

from parse import parse_trip_update, parse_vehicle_position

log_dir = "logs"
Path(log_dir).mkdir(parents=True, exist_ok=True)
logging.config.fileConfig("log_conf.ini")
logger = logging.getLogger(__name__)

def add_missing_slash(path):
    if path[-1] in ["/", "\\"]:
        return path

    return f"{path}/"


def save_updates(updates, path):
    """Saves a list of updates to the provided path.

    The stop updates are appended to an existing dataframe if it exists.

    :arg
        updates: a list of lists.
        path (str): the path where to save the updates.
    """
    if not updates:
        logger.info(f"Updates is empty or None, nothing to save: {updates}")

    logger.info("Creating dataframe.")
    columns = list(map(lambda field: field.name, dataclasses.fields(updates[0])))
    df_updates = pd.DataFrame(updates, columns=columns)

    if os.path.exists(path):
        existing_df = pd.read_feather(path)
        df_updates = pd.concat((existing_df, df_updates), ignore_index=True, axis=0)

    logger.info(f"Saving dataframe at {path}")
    df_updates.to_feather(path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Reading files')

    parser.add_argument('-i', '--in-path', type=str, required=True, help="Path to directory of .pb files.")
    parser.add_argument('-o', '--out-dir', type=str, required=True, help="Output directory where the parsed data will be saved.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose flag, will print out a tqdm loop.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--trip-updates", action="store_true", help="Parse trip updates.")
    group.add_argument("-p", "--vehicle-positions", action="store_true", help="Parse vehicle positions.")

    args = parser.parse_args()

    if args.trip_updates:
        out_name = "trip-updates.feather"
        parse_update = parse_trip_update
    elif args.vehicle_positions:
        out_name = "vehicle-positions.feather"
        parse_update = parse_vehicle_position
    else:
        logger.error(f"Either the stop updates (-t/--trip-updates) or vehicle positions (-p/--vehicle-positions) flag"
                     f"must be defined")
        exit(1)

    # add a slash to the provided path if it is missing
    in_path = add_missing_slash(args.in_path)
    out_dir = add_missing_slash(args.out_dir)

    logger.info(f"Creating output directory: {out_dir} if it does not exist yet.")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_path = f"{out_dir}{out_name}"

    files = glob.glob(f"{in_path}*.pb")
    logger.info(f"Found {len(files)} .pb files to read.")

    updates = []

    for i, file in tqdm(enumerate(files), disable=not args.verbose):
        with open(file, 'rb') as f:

            feed = gtfs_realtime_pb2.FeedMessage()

            try:
                feed.ParseFromString(f.read())
            except DecodeError as de:
                logger.warning(f"Could not parse {file}. {de}")

            updates += parse_update(feed)

        if i % 100 == 0 and i > 0:
            save_updates(updates, out_path)
            updates = []

    logger.info("Finished reading all files.")
    save_updates(updates, out_path)
