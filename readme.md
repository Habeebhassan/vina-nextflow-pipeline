# Nextflow AutoDock Vina HTVS Pipeline

This repository contains a High-Throughput Virtual Screening (HTVS) pipeline built with Nextflow, Docker, and AutoDock Vina. It automates the process of docking large libraries of ligands against target protein receptors, handling everything from raw data ingestion to physical parameterization, parallel docking execution, and final data aggregation.

## What It Does

The pipeline takes a raw protein structure (PDB) and a list of small molecules (SMILES strings) and performs the following automated steps:
1. Receptor Preparation: Cleans the PDB file by stripping water and heteroatoms, calculates the bounding box coordinates using a reference ligand, and adds Gasteiger charges and polar hydrogens to generate a PDBQT file.
2. Ligand Preparation: Converts 1D SMILES strings into 3D conformations using RDKit, optimizes the geometry using the Universal Force Field (UFF), and maps rotatable bonds using Meeko to output flexible PDBQT files.
3. Cross-Product Docking: Generates a Cartesian product of all receptors and ligands, spinning up parallel AutoDock Vina simulations for every pair.
4. Aggregation and Reporting: Collects all simulation logs, extracts the top binding affinities (kcal/mol), and compiles them into a summary CSV and a visual heatmap using Pandas and Seaborn.

## Features

* Fully Containerized: All dependencies (Python 3.11, OpenBabel, RDKit, Meeko, Biopython, AutoDock Vina) are locked inside a local Docker image for strict reproducibility.
* Asynchronous Execution: Built on Nextflow DSL2, allowing independent processes to run concurrently across all available CPU cores.
* Fault Tolerant: If one docking simulation fails, the pipeline continues processing the remaining compounds. The `-resume` flag allows restarting from the exact point of failure.
* Automated Search Space: Dynamically calculates the AutoDock grid box based on the co-crystallized reference ligand.

## Prerequisites

To run this pipeline, you must have the following installed on your host machine:
* Unix-based OS (Ubuntu, Debian, macOS)
* Nextflow (version 22.10.0 or higher)
* Docker Engine
* Git

## Installation and Setup

1. Clone the repository:
   git clone <your-repository-url>
   cd vina-nextflow-pipeline

2. Build the localized Docker image:
   The pipeline relies on a custom Docker image to avoid dependency conflicts. You must build this image locally before running the pipeline for the first time.
   docker build -t local/vina-prep:latest .

3. Grant execution permissions to the Python scripts:
   Nextflow requires the helper scripts in the bin/ directory to be executable.
   chmod +x bin/*.py

## How to Use

To execute the pipeline using the default test data (1IEP receptor vs. Aspirin and Imatinib):

nextflow run main.nf -profile docker

To resume a failed or interrupted run without recalculating successful steps, append the resume flag:

nextflow run main.nf -profile docker -resume

### Viewing Results

Once the pipeline completes, all output artifacts are saved in the `results/` directory:
* `results/prepared_receptors/`: Cleaned PDBs, grid box JSONs, and parameterized PDBQTs.
* `results/prepared_ligands/`: Flexible ligand PDBQT files.
* `results/docking_results/`: Raw AutoDock Vina simulation outputs and log files.
* `results/report/`: The final `docking_summary.csv` and `docking_heatmap.png`.

## Project Structure

* `main.nf`: The master Nextflow workflow script.
* `nextflow.config`: Global configuration defining the Docker profile and execution parameters.
* `Dockerfile`: The environment definition for the biological and chemical tools.
* `modules/`: Contains the Nextflow DSL2 process definitions (prep_receptor.nf, prep_ligand.nf, dock.nf, summarize.nf).
* `bin/`: Python helper scripts automatically mounted to the Nextflow $PATH (clean_pdb.py, prep_ligand.py, run_vina.py, parse_vina_logs.py).
* `assets/`: Directory for raw input files (e.g., PDB files).

## Troubleshooting

1. Error: command not found (e.g., clean_pdb.py: command not found)
Nextflow cannot execute the Python scripts in the `bin/` directory unless they have executable permissions. Run `chmod +x bin/*.py` from the project root.

2. ModuleNotFoundError or FileNotFoundError inside Nextflow
This indicates that the Nextflow process is bypassing Docker and running on your local OS, or the Docker image failed to build correctly. 
* Verify the image exists by running: `docker images | grep local/vina-prep`
* Ensure you are running the pipeline with the `-profile docker` flag.
* Check your `nextflow.config` to ensure `docker.enabled = true` is set.

3. WARN: Unrecognized config option 'docker.userEmulation'
This is a deprecation warning in newer versions of Nextflow. It does not break the pipeline. You can resolve it by updating your `nextflow.config` to use `docker.runOptions = '-u $(id -u):$(id -g)'` instead.

4. Network timeout during Docker build
Downloading large packages like RDKit can occasionally time out. The Dockerfile is configured with an extended timeout threshold, but if it fails, simply re-run the `docker build -t local/vina-prep:latest .` command.