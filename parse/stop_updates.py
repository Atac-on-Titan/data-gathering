"""Contains functions and classes for parsing stop updates."""
from dataclasses import dataclass


@dataclass
class StopUpdate:
    trip_id: str
    start_time: str
    start_date: str
    route_id: str
    stop_sequence: str
    delay: int
    time: int
    uncertainty: int
    stop_id: str

    @staticmethod
    def colnames():
        return ["trip_id", "start_time", "start_date", "route_id", "stop_sequence", "delay", "time", "uncertainty", "stop_id"]


def parse_stop_update(feed):
    """Parses a single stop update .pb file.

    :arg
        feed: the protobuffer GTFS feed,

    :return
        a list of lists, where each nested list represents a stop update.
    """

    stop_updates = []

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

                stop_update = StopUpdate(trip_id, start_time, start_date, route_id, stop_sequence, delay, time, uncertainty,
                               stop_id)

                stop_updates.append(stop_update)

    return stop_updates
