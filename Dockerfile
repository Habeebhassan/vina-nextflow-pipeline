FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OpenBabel and wget (for downloading the binary)
RUN apt-get update && apt-get install -y openbabel wget && rm -rf /var/lib/apt/lists/*

# Download the official AutoDock Vina CLI binary and make it executable
RUN wget https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.5/vina_1.2.5_linux_x86_64 -O /usr/local/bin/vina && \
    chmod +x /usr/local/bin/vina

# Install Python dependencies
RUN pip install --default-timeout=1000 --no-cache-dir rdkit meeko gemmi numpy scipy biopython vina pandas matplotlib seaborn