# Purpose
Gathering the necessary data from ATAC and other sources for the project.

# Python Scripts

## Downloading
There is a single python script that can be used to either download the **trip-updates** files, the **vehicle-positions**
files, or **historical weather** data. The downloaded files will be saved with the time of the download in the file name in the **specified output directory**.

The script also generates an `.log` file with log statements from the script in a `./logs` directory.

### Trip Updates
To download the trip updates:

```bash
python download_real_time.py -t="trip-updates" -o=<chosen output directory>
```

### Vehicle Positions
To download the vehicle positions:

```bash
python download_real_time.py -t="vehicle-positions" -o=<chosen output directory>
```

### Containerisation
The above mentioned python script has also been dockerised and can be run either with `docker` or `docker-compose`.

#### Docker

##### 1. Build
In the root directory, run the following command, replacing 

```bash
docker build -t <tag name> . 
```

##### 2. Run
Then run the built image, you need to pass the **type** `-t` and **output directory** `-o` parameters.

```bash
docker run <tag name> -e type=<type> -e output_dir=<output_dir> -v <type>:/app/<output_dir> -v logs:/app/logs
```

This starts a container and runs the script with the provided parameters. The downloaded files will be saved in the 
specifies **volume** which is created if it doesn't exist.

#### Docker Compose
Much easier than using straight docker, the `docker-compose.yml` contains services for starting a container for **vehicle-positions**
and **trip-updates**.

```bash
docker compose up
```

### Weather Data
The [download_historical_weather.py](download_historical_weather.py) script allows you to download **hourly historical
weather data** for the city of Rome, using the [OpenWeather API](https://openweathermap.org/history). The data is saved in the specified **output** directory. 
The OpenWeather API requires an **API key** (ask Jonas for it) to make requests. You need to create an `.env` file in the root
directory and add the API key in it for the script to work. The script will automatically pick up the file.

```
API_KEY=...
```

To run the script, you need to specify start time `-s` in UTC UNIX, end time `-e` in UTC UNIX, and the output directory
`-o`. The output directory is created if it does not exist. Replace `...` with your preferred values in the example below.

```bash
python download_historical_weather.py -s=... -e=... -o="..."
```

## Parsing
The [parse](parse.py) script reads all trip updates or vehicle positions `.pb` files in a provided directory and combines 
the entries into a pandas dataframe.

### How to run
1. Install requirements.
    ```
   pip install -r requirements.txt
   ```
1. Run `parse` script with flags for the input `-i` and output directory `-o`. The output directory is created if it 
    does not exist. In the example below, replace `...`
    with the path to the directory. The `-v` flag prints out the `tqdm` loop. You also have to specify whether you want
    parse **trip-updates** (`-t`) or **vehicle-positions** (`-p`).
    ```
   python read.py -i="..." -o="..." -t
   ```
   For example, if the `.pb` files are in a `data/trip-updates/` and I want the output data frame to be in the current
    directory, you can run the script as follows:
    ```
   python read.py -i="data/trip-updates" -o="./" -t
   ```

The output is a `.feather` file in the specified output directory that contains the following columns for trip updates:

| trip_id | start_time | start_data | route_id | stop_sequence | delay | time | uncertainty | stop_id |
|---------|------------|------------|----------|---------------|-------|------|-------------|---------|
|         |            |            |          |               |       |      |             |         |


and the following for vehicle positions:

| vehicle_id | label | trip_id | route_id | direction_id | start_time | start_date | current_stop_sequence | stop_id | current_status | timestamp | latitude | longitude | odometer |
|------------|-------|---------|----------|--------------|------------|------------|-----------------------|---------|----------------|-----------|----------|-----------|----------|
