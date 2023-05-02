#!bin/bash

output_dir="$(dirname -- $0)"/trip-updates

echo "Writing into: $output_dir"

mkdir -p "$output_dir"

datetime=$(date '+%Y-%m-%d-%H-%M-%S')

wget -O "$output_dir"/rome_trip_updates_"$datetime".pb https://dati.comune.roma.it/catalog/dataset/a7dadb4a-66ae-4eff-8ded-a102064702ba/resource/bf7577b5-ed26-4f50-a590-38b8ed4d2827/download/rome_trip_updates.pb
