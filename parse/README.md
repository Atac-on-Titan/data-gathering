# Purpose
The purpose of this package is provide logic for parsing `.pb` files.

# Stop Updates
To parse stop updates `.pb` files, you can use the `parse_trip_update` function. The function returns a `StopUpdate` object.

```python
from parse import parse_trip_update

feed = <your trip update feed>

parse_trip_update(feed)
```

# Vehicle Locations
To parse vehicle location `.pb` files, you can use the `parse_vehicle_locations` function. The function
returns a `VehiclePosition` object.

```python
from parse import parse_vehicle_position

feed = <your vehicle position feed>

parse_vehicle_position(feed)
```
