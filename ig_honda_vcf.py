import subprocess
import os
from multiprocessing import Pool
import argparse
from functools import partial



#IMGT_alleles = "/home/egenge01/anaconda3/envs/IGv2/lib/python2.7/site-packages/IGenotyper-1.1-py2.7.egg/IGenotyper/data/alleles.fasta"

def run_do_vcfs(files,rpath):
    with open(files, "r") as file:
        samples = [line.strip().split()[0] for line in file]

    # Run function in parallel
    with Pool() as pool:
        pool.map(partial(run_do_vcf, rpath=rpath), samples)


def run_do_vcf(sample,rpath):
    print(f"Processing sample {sample}")

    output_dir = os.path.join(rpath, "variant_analysis", sample)
    #os.makedirs(output_dir, exist_ok=True)
    #creating directories should be handled by a helper somewhere else, but I'll leave it here for now

    bam_path = f"{rpath}/variant_analysis/{sample}/{sample}_editRG.bam"
    mpileup_path = f"{rpath}/variant_analysis/{sample}/{sample}_mpileup.vcf.gz"
    called_vcf = f"{rpath}/variant_analysis/{sample}/{sample}_called.vcf"
    called_vcf_gz = f"{rpath}/variant_analysis/{sample}/{sample}_called.vcf.gz"

    
    # These should be switched to list rather than strings... but its fine if you dont add ""; rm -rf /"" as an argument... shell injection vulnerability
    # Fix before making public
    try:
        subprocess.run(f"bcftools mpileup -Ou --no-BAQ -q 0 -Q 0 -f {reffn} {bam_path} -R {rpath}/regions/IGK_CJV_nodropout.bed | bgzip -c > {mpileup_path}", shell=True, check=True)
        subprocess.run(f"bcftools index -f {mpileup_path}", shell=True, check=True)
        subprocess.run(f"bcftools call -R {rpath}/regions/IGK_CJV_nodropout.bed -m -Ov -o {called_vcf} {mpileup_path}", shell=True, check=True)
        subprocess.run(f"bgzip -c {called_vcf} > {called_vcf_gz}", shell=True, check=True)
        subprocess.run(f"tabix {called_vcf_gz}", shell=True, check=True)
        subprocess.run(f"bcftools index {called_vcf_gz}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error {e.returncode}")

if __name__ == "__main__":
    print("vcf was started")
    #these constant paths may want to be moved to function, but that may cause issues when importing the function somewhere else.. best not to for future modularity. best to pass these to the function
    gene_coords = "/home/zmvanw01/genome/igv2_references/gene_coords.bed"
    reffn = "/home/zmvanw01/genome/igv2_references/reference.fasta"
    extract_seq = "/home/zmvanw01/genome/igv2_references/extract_sequence_from_bam_EEmod3.py"
    argparser = argparse.ArgumentParser(description='Run variant analysis.')
    argparser.add_argument('--file', '-f', type=str, help='Path to the .txt file containing sample IDs', required=True)
    argparser.add_argument('--outdir', '-o', type=str, help='Output directory', default=os.getcwd())
    args = argparser.parse_args()
    rpath = args.outdir
    sample_file_path = args.file
    print(sample_file_path)
    #output_directory = args.outdir
    run_do_vcfs(sample_file_path,rpath)