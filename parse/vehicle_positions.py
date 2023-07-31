"""Module for parsing vehicle positions."""
from dataclasses import dataclass


@dataclass
class VehiclePosition:
    vehicle_id: str
    label: str
    trip_id: str
    route_id: str
    direction_id: int
    start_time: str
    start_date: str
    current_stop_sequence: int
    stop_id: int
    current_status: str
    timestamp: int
    latitude: float
    longitude: float
    odometer: int


def parse_vehicle_position(feed):
    """Parses vehicle positions from a GTFS feed.

    :arg
        feed: the GTFS feed from a .pb file.

    return:
        a list of VehiclePosition objects.
    """

    vehicle_positions = []

    for entity in feed.entity:
        id = entity.id
        vehicle = entity.vehicle
        trip = vehicle.trip
        position = vehicle.position

        vehicle_position = VehiclePosition(vehicle.vehicle.id, vehicle.vehicle.label, trip.trip_id, trip.route_id, trip.direction_id,
                            trip.start_time, trip.start_date, vehicle.current_stop_sequence, vehicle.stop_id,
                            vehicle.current_status, vehicle.timestamp, position.latitude, position.longitude,
                            position.odometer)

        vehicle_positions.append(vehicle_position)

    return vehicle_positions

