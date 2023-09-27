import argparse
import os
from ig_honda_helper import generate_sbatch, submit_sbatch, count_lines
#from ig_honda_vcf import run_do_vcfs, run_do_vcf

def main():
    # Initialize argparse
    parser = argparse.ArgumentParser(description='Run variant analysis.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the .txt file containing sample IDs.')
    parser.add_argument('-o', '--outdir', type=str, default='.', help='Output directory for results.')
    parser.add_argument('--sbatch', type=str, choices=['keep', 'remove'], default='remove', help='Whether to keep or remove the sbatch file.')
    parser.add_argument('--alleles', '-a', type=str, default='0')
    args = parser.parse_args()

    sample_file_path = args.file
    output_directory = args.outdir
    num_samples = count_lines(sample_file_path)

    # Limit cores to a maximum of 144 (12 nodes * 12 threads)
    num_cores = min(num_samples, 144)
    print("The number of cores is " + str(num_cores))
    # Generate the sbatch file and submit it
    generate_sbatch(num_cores, sample_file_path, output_directory)
    result = submit_sbatch()
    print(f"Sbatch submission result: {result}")

    

    # Remove the sbatch file if the user didn't specify to keep it
    if args.sbatch == 'remove':
        os.remove("dynamic_sbatch.sbatch")
        print("Removed dynamic_sbatch.sbatch")

if __name__ == '__main__':
    main()
