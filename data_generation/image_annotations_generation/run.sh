#!/bin/bash

# Function to read the value of the first line in the TOML file for a given key
get_value_from_toml() {
    toml_file=$1
    # Extract the value of the first line and remove any surrounding spaces or quotes
    value=$(head -n 1 "$toml_file" | sed -n "s/conda_env_name\s*=\s*'\([^']*\)'/\1/p")
    echo $value
}

# Path to the TOML configuration file
config_file="config.toml"

# Get the conda environment name from the config.toml file
conda_env_name=$(get_value_from_toml "$config_file")

# Check if the conda environment name was retrieved
if [ -z "$conda_env_name" ]; then
    echo "Error: Conda environment name not found in config.toml"
    exit 1
fi

# Activate the specified conda environment
echo "Activating conda environment: $conda_env_name"
source ~/anaconda3/etc/profile.d/conda.sh  # Adjust this if your conda is located elsewhere
conda activate "$conda_env_name" && python main.py

# Deactivate the conda environment after running the script
conda deactivate
