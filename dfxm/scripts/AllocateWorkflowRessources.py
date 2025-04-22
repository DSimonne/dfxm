import os
import argparse
import subprocess

def create_slurm_script(
    hdf5_file, 
    graph,
    darfix_version="2.4",
):
    "Create a `.slurm` file to run the workflow as a SLURM job."
    
    work_dir = os.path.dirname(hdf5_file)
    print(f"Using darfix/{darfix_version}")
    
    # Define slurm file content
    slurm_script_content = "#!/bin/bash" \
    "\n#SBATCH --job-name=darfix_job_%j" \
    f"\n#SBATCH --output={work_dir}/darfix_job_%j.out" \
    f"\n#SBATCH --error={work_dir}/darfix_job_%j.err" \
    "\n#SBATCH --ntasks=1" \
    "\n#SBATCH --mem=400G" \
    "\n#SBATCH --time=1:00:00" \
    "\n#SBATCH --cpus-per-task=20" \
    f"\nmodule load darfix/{darfix_version}" \
    f"\npython RunDarfixWorkflow.py '{hdf5_file}' '{graph}'"

    # Define slurm file path
    slurm_script_path = os.path.join(
        work_dir,
        f"darfix_job.slurm"
    )
    # Save slurm file content
    with open(slurm_script_path, "w") as f:
        f.write(slurm_script_content)
            
    return slurm_script_path

def main(hdf5_file, graph):
    slurm_script_path = create_slurm_script(hdf5_file, graph)
    subprocess.run(["sbatch", slurm_script_path])
    print(f"Using {hdf5_file} as input file and {graph} as graph.")
    print(f"Saved slurm script as {slurm_script_path}")
    print("Follow job evolution with `squeue --job <job_id>`\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute a Darfix workflow as SLURM jobs."
    )
    parser.add_argument(
        "hdf5_file", 
        type=str, 
        help="Path to the HDF5 input file."
    )
    parser.add_argument(
        "graph", 
        type=str, 
        help="Path to the workflow graph file."
    )
    
    args = parser.parse_args()
    main(args.hdf5_file, args.graph)
