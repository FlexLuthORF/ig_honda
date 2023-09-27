import subprocess
import os
from multiprocessing import Pool
import argparse
from functools import partial

def run_do_allele(sample, rpath, IMGT_alleles, gene_coords, extract_seq):
    print(f"Processing sample {sample}")

    output_dir = os.path.join(rpath, "alleles_from_contigs_blat", sample)
    os.makedirs(output_dir, exist_ok=True)
    
    blat_out = os.path.join(output_dir, f"{sample}_IMGT_blat_res.txt")

    try:
        subprocess.run(f"/home/egenge01/blat/blat {IMGT_alleles} {rpath}/alleles_from_contigs/{sample}/{sample}_allele_seqs.fasta -out=blast8 {blat_out}", shell=True, check=True)
        subprocess.run(f"Rscript parse_blast_output10.R {blat_out} {sample} {rpath}/alleles_from_contigs/parse_blat/{sample}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error {e.returncode}")

def run_do_alleles(files, rpath, IMGT_alleles, gene_coords, extract_seq):
    with open(files, "r") as file:
        samples = [line.strip().split()[0] for line in file]

    with Pool() as pool:
        pool.map(partial(run_do_allele, rpath=rpath, IMGT_alleles=IMGT_alleles, gene_coords=gene_coords, extract_seq=extract_seq), samples)

def run_concatenate(rpath):
    all_samples_path = os.path.join(rpath, "alleles_from_contigs", "parse_blat", "concatenate", "all_samples.txt")
    if os.path.exists(all_samples_path):
        os.remove(all_samples_path)

    with open("36_samp_groups.txt", "r") as file:
        for line in file:
            sample, pop = line.strip().split()
            if sample not in ["NA19467", "NA18522", "HG01925", "HG02018"]:
                os.makedirs(os.path.join(rpath, "alleles_from_contigs", "parse_blat", "concatenate"), exist_ok=True)
                with open(all_samples_path, 'a') as all_samples_file:
                    with open(f"{rpath}/alleles_from_contigs/parse_blat/{sample}/{sample}_IGK.vs.IMGT_consolidated.txt", 'r') as sample_file:
                        all_samples_file.write(sample_file.read())

if __name__ == "__main__":
    print("Alleles was started")

    IMGT_alleles = "/home/zmvanw01/genome/igv2_references/alleles.fasta"
    gene_coords = "/home/zmvanw01/genome/igv2_references/gene_coords.bed"
    extract_seq = "/home/zmvanw01/genome/igv2_references/extract_sequence_from_bam_EEmod3.py"

    argparser = argparse.ArgumentParser(description='Run allele analysis.')
    argparser.add_argument('--file', '-f', type=str, help='Path to the .txt file containing sample IDs', required=True)
    argparser.add_argument('--outdir', '-o', type=str, help='Output directory', default=os.getcwd())
    args = argparser.parse_args()

    rpath = args.outdir
    sample_file_path = args.file

    run_do_alleles(sample_file_path, rpath, IMGT_alleles, gene_coords, extract_seq)
