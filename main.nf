nextflow.enable.dsl = 2

include { PREP_RECEPTOR }     from './modules/prep_receptor.nf'
include { PREP_LIGAND }       from './modules/prep_ligand.nf'
include { DOCK_VINA }         from './modules/dock.nf'
include { SUMMARIZE_RESULTS } from './modules/summarize.nf'

workflow {
    receptor_ch = Channel.of( tuple("1IEP", file("${projectDir}/assets/1iep.pdb"), "STI") )
    ligand_ch   = Channel.of( 
        tuple("aspirin", "CC(=O)OC1=CC=CC=C1C(=O)O"),
        tuple("imatinib", "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5") 
    )

    PREP_RECEPTOR(receptor_ch)
    PREP_LIGAND(ligand_ch)

    docking_pairs_ch = PREP_RECEPTOR.out.receptor_data.combine(PREP_LIGAND.out.pdbqt)
    DOCK_VINA(docking_pairs_ch)
    
    // Extract just the log files from the DOCK_VINA output tuple, collect them into a list, and summarize
    log_files_ch = DOCK_VINA.out.results.map { row -> row[3] }.collect()
    SUMMARIZE_RESULTS(log_files_ch)
}