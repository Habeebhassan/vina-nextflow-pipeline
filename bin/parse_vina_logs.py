#!/usr/bin/env python3
import sys
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def parse_logs(log_files):
    results = []
    
    for log_path in log_files:
        # Extract receptor and ligand from filename (e.g., 1IEP_aspirin.log)
        filename = log_path.split('/')[-1].replace('.log', '')
        parts = filename.split('_')
        receptor = parts[0]
        ligand = parts[1] if len(parts) > 1 else "unknown"
        
        affinity = None
        with open(log_path, 'r') as f:
            for line in f:
                # Match the first mode (best score) line
                # Format: "   1        -9.8      0.000      0.000"
                if re.match(r'^\s*1\s+', line):
                    affinity = float(line.split()[1])
                    break
                    
        if affinity is not None:
            results.append({"Receptor": receptor, "Ligand": ligand, "Affinity_kcal_mol": affinity})
            
    return pd.DataFrame(results)

if __name__ == "__main__":
    logs = glob.glob("*.log")
    if not logs:
        sys.exit("No log files found.")
        
    df = parse_logs(logs)
    
    # Save CSV
    df.to_csv("docking_summary.csv", index=False)
    print("Generated docking_summary.csv")
    
    # Generate Heatmap (Receptors on Y, Ligands on X)
    pivot_df = df.pivot(index="Receptor", columns="Ligand", values="Affinity_kcal_mol")
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_df, annot=True, cmap="coolwarm", center=0, cbar_kws={'label': 'Binding Affinity (kcal/mol)'})
    plt.title("AutoDock Vina Binding Affinities")
    plt.tight_layout()
    plt.savefig("docking_heatmap.png", dpi=300)
    print("Generated docking_heatmap.png")