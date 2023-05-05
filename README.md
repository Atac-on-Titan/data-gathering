# Purpose
Gathering the necessary data from ATAC and other sources for the project.

# Python Scripts
There is a single python script that can be used to either download the **trip-updates** files or the **vehicle-positions**
files. The downloaded files will be saved with the time of the download in the file name in the **specified output directory**.

The script also generates an `app.log` file with log statements from the script.

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
