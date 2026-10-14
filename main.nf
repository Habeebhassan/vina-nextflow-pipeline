nextflow.enable.dsl = 2

// Import our module
include { PREP_LIGAND } from './modules/prep_ligand.nf'

workflow {
    // 1. Define our test data channel
    ligand_ch = Channel.of(
        tuple("aspirin", "CC(=O)OC1=CC=CC=C1C(=O)O"),
        tuple("imatinib", "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5")
    )
    
    // 2. Feed it into the process
    PREP_LIGAND(ligand_ch)
}
