# Purpose
The purpose of the `download` package is to expose methods for downloading the raw data that we need for the project.

# Downloading Trip Updates
To download the trip updates, you can use the `download_trip_updates` function. This will download the `proto buffer`
file and return the **binary response content**.

```python
from download import download_trip_updates

trip_updates = download_trip_updates()
```

# Downloading Vehicle Positions
To download the vehicle positions, you can use the `download_vehicle_positions` function. This will download the `proto buffer`
file and return the **binary response content**.

```python
from download import download_vehicle_positions

trip_updates = download_vehicle_positions()
```