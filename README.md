# Purpose
Gathering the necessary data from ATAC and other sources for the project.

# Python Scripts
There is a single python script that can be used to either download the **trip-updates** files or the **vehicle-positions**
files. The downloaded files will be saved with the time of the download in the file name in the **specified output directory**.

The script also generates an `.log` file with log statements from the script in a `./logs` directory.

## Trip Updates
To download the trip updates:

```bash
python download_real_time.py -t="trip-updates" -o=<chosen output directory>
```

## Vehicle Positions
To download the vehicle positions:

```bash
python download_real_time.py -t="vehicle-positions" -o=<chosen output directory>
```

# Containerisation
The above mentioned python script has also been dockerised and can be run either with `docker` or `docker-compose`.

## Docker

### 1. Build
In the root directory, run the following command, replacing 

```bash
docker build -t <tag name> . 
```

### 2. Run
Then run the built image, you need to pass the **type** `-t` and **output directory** `-o` parameters.

```bash
docker run <tag name> -e type=<type> -e output_dir=<output_dir> -v <type>:/app/<output_dir> -v logs:/app/logs
```

This starts a container and runs the script with the provided parameters. The downloaded files will be saved in the 
specifies **volume** which is created if it doesn't exist.

## Docker Compose
Much easier than using straight docker, the `docker-compose.yml` contains services for starting a container for **vehicle-positions**
and **trip-updates**.

```bash
docker compose up
```