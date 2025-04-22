#!/bin/bash

# List of directories
directories=(
    "Fe_22440003_strain_proj_10x"
    "Fe_22440003_strain_proj_10x__corrosion_step_1"
    "Fe_22440003_strain_proj_10x__corrosion_step_2"
    "Fe_22440003_strain_proj_10x__corrosion_step_3"
    "Fe_22440003_strain_proj_10x__corrosion_step_4"
    "Fe_22440003_strain_proj_2x_redo_3"
    "Fe_22440003_strain_proj_2x__corrosion_step_1_redo_2"
    "Fe_22440003_strain_proj_2x__corrosion_step_2_redo_again"
    "Fe_22440003_strain_proj_2x__corrosion_step_3"
    "Fe_22440003_strain_proj_2x__corrosion_step_4"
)

# Iterate through the list of directories
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "Entering $dir"
        
        # Remove the 'fit' folder if it exists
        rm -rf "$dir/fit"
        
        # Remove certain files in the directory
        find "$dir" -maxdepth 1 -type f -name "*.txt" -delete
        find "$dir" -maxdepth 1 -type f -name "maps.h5" -delete
        find "$dir" -maxdepth 1 -type f -name "data.hdf5" -delete
        find "$dir" -maxdepth 1 -type f -name "*.err" -delete
        find "$dir" -maxdepth 1 -type f -name "*.out" -delete
        find "$dir" -maxdepth 1 -type f -name "*.slurm" -delete
        
        # mkdir $dir/Figures
        echo "Cleaned $dir"
    else
        echo "Directory $dir not found. Skipping."
    fi
done

echo "Cleanup complete."
