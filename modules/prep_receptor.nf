nextflow.enable.dsl = 2

process PREP_RECEPTOR {
    tag "${receptor_id}"
    container 'local/vina-prep:latest'
    
    publishDir "${params.outdir}/prepared_receptors", mode: 'copy'

    input:
    tuple val(receptor_id), path(pdb_file), val(ref_ligand)

    output:
    tuple val(receptor_id), path("${receptor_id}_clean.pdbqt"), path("box.json"), emit: receptor_data

    script:
    """
    # 1. Clean PDB & calculate grid box
    clean_pdb.py --pdb "${pdb_file}" --out "${receptor_id}_clean.pdb" --ligand "${ref_ligand}"
    
    # 2. Add polar hydrogens, assign Gasteiger charges, and output PDBQT
    obabel "${receptor_id}_clean.pdb" -O "${receptor_id}_clean.pdbqt" -xr
    """
}