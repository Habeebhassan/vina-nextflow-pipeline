#!/usr/bin/env python3
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation, PDBQTWriterLegacy

# 1. Load Aspirin SMILES
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol)

# 2. Generate 3D coordinates
AllChem.EmbedMolecule(mol)
AllChem.UFFOptimizeMolecule(mol)

# 3. Prepare for AutoDock (Using the modern Meeko v0.5+ API)
preparator = MoleculePreparation()
mol_setups = preparator.prepare(mol)

# 4. Write output using the new Legacy Writer
pdbqt_string, is_ok, error_msg = PDBQTWriterLegacy.write_string(mol_setups[0])

if is_ok:
    with open("/data/aspirin_test.pdbqt", "w") as f:
        f.write(pdbqt_string)
    print("PDBQT generated successfully!")
else:
    print(f"Failed: {error_msg}")
