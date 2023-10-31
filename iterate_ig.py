import os
import subprocess
from multiprocessing import Pool
import argparse
from functools import partial

def run_IG_for_sample(rpath,sample_data):
    sample, data_path = sample_data
    command = f"bash run_IG.sh {sample} {data_path} {rpath}"
    subprocess.run(command, shell=True)
def run_do_igks(files, rpath):
    
    with open(files, "r") as file:
        sample_data = [tuple(line.strip().split()) for line in file]

    with Pool(processes=10) as pool:
        pool.map(partial(run_IG_for_sample, rpath=rpath), sample_data)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Run IG analysis.')
    argparser.add_argument('--file', '-f', type=str, help='Path to the .txt file containing sample IDs', required=True)
    argparser.add_argument('--outdir', '-o', type=str, help='Output directory', default=os.getcwd())
    
    args = argparser.parse_args()
    rpath = args.outdir
    sample_file_path = args.file
    
    print(sample_file_path)
    run_do_igks(sample_file_path, rpath)