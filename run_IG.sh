function run_IG {
    export SJOB_DEFALLOC=NONE
    sample=$1
    data_path=$2
    outdir=$3
    
    mkdir -p ${outdir}/run_igenotyper2
    mkdir -p ${outdir}/IG_jobs

    if [ -d "${outdir}/run_igenotyper2/${sample}/tmp" ]; then
        echo "Directory ${outdir}/run_igenotyper2/${sample}/tmp exists. Skipping ${sample}..."
        return
    fi

    file1="${outdir}/run_igenotyper/$sample/tmp/ccs.fasta"
    file2="${outdir}/run_igenotyper/$sample/alignments/ccs_to_ref_phased.sorted.bam"

    if [ -e "$file1" ] || [ -e "$file2" ]; then
        echo "Either $file1 or $file2 exists for sample $sample. Skipping..."
        return
    fi

    samtools index ${data_path}

    IG phase \
        --sample ${sample} \
        --threads 12 \
        ${data_path} \
        ${outdir}/run_igenotyper2/${sample}

    IG assembly \
        --threads 12 \
        ${outdir}/run_igenotyper2/${sample}
}

run_IG $@
