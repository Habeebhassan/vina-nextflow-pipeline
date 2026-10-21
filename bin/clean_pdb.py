#!/usr/bin/env python3
import argparse
import json
import numpy as np
from Bio import PDB
import sys

def clean_and_get_box(pdb_in, pdb_out, ref_ligand_resname):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_in)
    
    ligand_coords = []
    
    # Define a filter to strip out noise
    class CleanSelect(PDB.Select):
        def accept_residue(self, residue):
            resname = residue.get_resname().strip()
            # 1. Exclude water
            if resname in ["HOH", "WAT"]:
                return 0
            # 2. Extract coordinates of the old drug, but delete it from the final structure
            if resname == ref_ligand_resname:
                for atom in residue:
                    ligand_coords.append(atom.get_coord())
                return 0
            # 3. Exclude buffer salts and other heteroatoms
            if residue.id[0] != " ":
                return 0
            return 1

    # Save the cleaned protein
    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save(pdb_out, CleanSelect())
    
    # Calculate the Grid Box center
    if not ligand_coords:
        sys.exit(f"Error: Reference ligand {ref_ligand_resname} not found in {pdb_in}. Cannot calculate grid box.")
        
    center = np.mean(ligand_coords, axis=0).tolist()
        
    box_config = {
        "center_x": round(center[0], 3),
        "center_y": round(center[1], 3),
        "center_z": round(center[2], 3),
        "size_x": 20.0,
        "size_y": 20.0,
        "size_z": 20.0
    }
    
    # Export coordinates for Nextflow to pass to Vina
    with open("box.json", "w") as f:
        json.dump(box_config, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdb", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--ligand", required=True, help="3-letter code of the co-crystallized ligand")
    args = parser.parse_args()
    
    clean_and_get_box(args.pdb, args.out, args.ligand)