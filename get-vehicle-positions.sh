#!bin/bash

output_dir="$(dirname -- $0)"/vehicle-positions

echo "Writing into: $output_dir"

mkdir -p "$output_dir"

datetime=$(date '+%Y-%m-%d-%H-%M-%S')

wget -O "$output_dir"/rome_vehicle_positions_"$datetime".pb https://dati.comune.roma.it/catalog/dataset/a7dadb4a-66ae-4eff-8ded-a102064702ba/resource/d2b123d6-8d2d-4dee-9792-f535df3dc166/download/rome_vehicle_positions.pb
