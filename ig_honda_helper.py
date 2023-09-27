import subprocess
import os

def count_lines(file_path):
    try:
        with open(file_path, "r") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return 0
def generate_sbatch(num_cores, sample_file, out_dir):
    sbatch_content = f"""#!/bin/bash
#SBATCH --job-name=variant_analysis
#SBATCH --partition=compute             # Partition (job queue)
#SBATCH --time=01:00:00              # Runtime in D-HH:MM format
#SBATCH --output=job_logs/%j.out     # File to which STDOUT will be written
#SBATCH --error=job_logs/%j.err      # File to which STDERR will be written
#SBATCH --ntasks-per-node=12
#SBATCH --ntasks={num_cores}
echo "Starting job for {sample_file} with {num_cores} cores."

python /home/zmvanw01/ig_honda/ig_honda_vcf.py --file {sample_file} --outdir {out_dir}

echo "Job finished."

"""

#ig_honda_vcf should be replaced with an argument at some point based on which comman dof ig_honda the user wants to run
    with open("dynamic_sbatch.sbatch", "w") as f:
        f.write(sbatch_content)
    #print(f"Generated sbatch content:\n{sbatch_content}")
def submit_sbatch():
    result = subprocess.run("sbatch dynamic_sbatch.sbatch", shell=True)
    if result.returncode != 0:
        print(f"Sbatch submission failed with error code {result.returncode}")
    return result.returncode
