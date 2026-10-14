nextflow.enable.dsl = 2

process PREP_LIGAND {
    tag "${ligand_id}"
    container 'local/vina-prep:latest'
    
    publishDir "${params.outdir}/prepared_ligands", mode: 'copy'

    input:
    tuple val(ligand_id), val(smiles)

    output:
    tuple val(ligand_id), path("${ligand_id}.pdbqt"), emit: pdbqt

    script:
    """
    # Execute our custom script
    prep_ligand.py --id "${ligand_id}" --smiles "${smiles}" --out "${ligand_id}.pdbqt"    
    """
}

// Standalone test entrypoint
workflow {
    params.outdir = 'results'
    
    Channel.of(
        tuple("aspirin", "CC(=O)OC1=CC=CC=C1C(=O)O"),
        tuple("imatinib", "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5")
    )
    | PREP_LIGAND
}
