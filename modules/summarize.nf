nextflow.enable.dsl = 2

process SUMMARIZE_RESULTS {
    container 'local/vina-prep:latest'
    
    publishDir "${params.outdir}/report", mode: 'copy'

    input:
    path logs

    output:
    path "docking_summary.csv"
    path "docking_heatmap.png"

    script:
    """
    parse_vina_logs.py
    """
}