#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receptor", required=True)
    parser.add_argument("--ligand", required=True)
    parser.add_argument("--box", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()

    # Read the grid box coordinates calculated in Phase 1
    with open(args.box, "r") as f:
        box = json.load(f)

    # Construct the AutoDock Vina command
    cmd = [
        "vina",
        "--receptor", args.receptor,
        "--ligand", args.ligand,
        "--center_x", str(box["center_x"]),
        "--center_y", str(box["center_y"]),
        "--center_z", str(box["center_z"]),
        "--size_x", str(box["size_x"]),
        "--size_y", str(box["size_y"]),
        "--size_z", str(box["size_z"]),
        "--exhaustiveness", "8",
        "--out", args.out
    ]

    print(f"Executing: {' '.join(cmd)}")
    
    # Run Vina and pipe the output to our log file
    with open(args.log, "w") as log_file:
        result = subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT)

    if result.returncode != 0:
        sys.exit(f"Vina docking failed for {args.ligand} on {args.receptor}")

if __name__ == "__main__":
    main()