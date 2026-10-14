#!/usr/bin/env python3
import sys
import argparse
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation, PDBQTWriterLegacy

def smiles_to_pdbqt(ligand_id: str, smiles: str, output_path: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        sys.exit(f"Error: Could not parse SMILES for {ligand_id}")

    mol = Chem.AddHs(mol)
    
    # Generate 3D coordinates
    AllChem.EmbedMolecule(mol, randomSeed=42)
    try:
        AllChem.UFFOptimizeMolecule(mol, maxIters=500)
    except Exception as e:
        print(f"Warning: UFF optimization failed for {ligand_id}: {e}", file=sys.stderr)

    # Prepare for AutoDock (Modern Meeko API)
    preparator = MoleculePreparation()
    mol_setups = preparator.prepare(mol)
    
    pdbqt_string, is_ok, error_msg = PDBQTWriterLegacy.write_string(mol_setups[0])
    
    if is_ok:
        with open(output_path, "w") as f:
            f.write(pdbqt_string)
        print(f"Successfully generated: {output_path}")
    else:
        sys.exit(f"Meeko failed for {ligand_id}: {error_msg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--smiles", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    
    smiles_to_pdbqt(args.id, args.smiles, args.out)
