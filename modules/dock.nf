nextflow.enable.dsl = 2

process DOCK_VINA {
    tag "${receptor_id} + ${ligand_id}"
    container 'local/vina-prep:latest'
    
    // Fixed: Pointing to a flat directory avoids the compilation error
    publishDir "${params.outdir}/docking_results", mode: 'copy'

    input:
    tuple val(receptor_id), path(receptor_pdbqt), path(box_json), val(ligand_id), path(ligand_pdbqt)

    output:
    tuple val(receptor_id), val(ligand_id), path("${receptor_id}_${ligand_id}_docked.pdbqt"), path("${receptor_id}_${ligand_id}.log"), emit: results

    script:
    """
    run_vina.py \\
        --receptor "${receptor_pdbqt}" \\
        --ligand "${ligand_pdbqt}" \\
        --box "${box_json}" \\
        --out "${receptor_id}_${ligand_id}_docked.pdbqt" \\
        --log "${receptor_id}_${ligand_id}.log"
    """
}