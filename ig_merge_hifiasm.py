import os
import subprocess
from multiprocessing import Pool
import argparse
from functools import partial

def merge(sample, dir_path, reffn):
    outdir = os.path.join(dir_path, sample, 'merged_bam', 'alg_asm20_to_ref')
    if not os.path.exists(os.path.join(outdir, f"{sample}.sorted.bam")):
        os.makedirs(outdir, exist_ok=True)

        merged_bam = os.path.join(dir_path, sample, 'softclipped_merged_bam', 'softclipped_merged.bam')
        merged_sorted_bam = os.path.join(dir_path, sample, 'softclipped_merged_bam', 'softclipped.merged.sorted.bam')
        merged_fasta = os.path.join(dir_path, sample, 'softclipped_merged_bam', 'softclipped_merged_all_reads.fasta')
        merged_rmdup_fasta = os.path.join(dir_path, sample, 'softclipped_merged_bam', 'softclipped_merged_all_reads.rmdup.fasta')

        bam1 = os.path.join(dir_path, sample, 'break_at_soft_clip', '2', '1_asm20_hifi_asm_to_ref.sorted.bam')
        bam2 = os.path.join(dir_path, sample, 'break_at_soft_clip', '2', '2_asm20_hifi_asm_to_ref.sorted.bam')
        
        subprocess.run(f"samtools merge -f {merged_bam} {bam1} {bam2}", shell=True)
        subprocess.run(f"samtools sort {merged_bam} -o {merged_sorted_bam}", shell=True)
        subprocess.run(f"samtools index {merged_sorted_bam}", shell=True)
        subprocess.run(f"samtools fasta --reference {reffn} {merged_sorted_bam} > {merged_fasta}", shell=True)
        subprocess.run(f"seqkit rmdup --by-seq {merged_fasta} -o {merged_rmdup_fasta}", shell=True)
#merging non-softclipped bams. Are these the right files?
        merged_bam = os.path.join(dir_path, sample, 'merged_bam', 'merged.bam')
        merged_sorted_bam = os.path.join(dir_path, sample, 'merged_bam', '.merged.sorted.bam')
        merged_fasta = os.path.join(dir_path, sample, 'merged_bam', 'merged_all_reads.fasta')
        merged_rmdup_fasta = os.path.join(dir_path, sample, 'merged_bam', 'merged_all_reads.rmdup.fasta')

        bam1 = os.path.join(dir_path, sample, 'hifiasm',  'asm.bp.hap1.p_ctg_to_ref.sorted.bam')
        bam2 = os.path.join(dir_path, sample, 'hifiasm', 'asm.bp.hap2.p_ctg_to_ref.sorted.bam')
        
        subprocess.run(f"samtools merge -f {merged_bam} {bam1} {bam2}", shell=True)
        subprocess.run(f"samtools sort {merged_bam} -o {merged_sorted_bam}", shell=True)
        subprocess.run(f"samtools index {merged_sorted_bam}", shell=True)
        subprocess.run(f"samtools fasta --reference {reffn} {merged_sorted_bam} > {merged_fasta}", shell=True)
        subprocess.run(f"seqkit rmdup --by-seq {merged_fasta} -o {merged_rmdup_fasta}", shell=True)

def run_merge(samples_file, dir_path, reffn):
    with open(samples_file, 'r') as file:
        samples = [line.strip() for line in file if 'HG00136' in line]
        
    # Run function in parallel
    with Pool() as pool:
        pool.map(partial(merge, dir_path=dir_path, reffn=reffn), samples)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Run merging process.')
    argparser.add_argument('--file', '-f', type=str, help='Path to the .txt file containing sample IDs', required=True)
    argparser.add_argument('--dir', '-d', type=str, help='Base directory', required=True)
    argparser.add_argument('--reffn', '-r', type=str, help='Path to the reference fasta file', required=True)

    args = argparser.parse_args()
    
    run_merge(args.file, args.dir, args.reffn)
