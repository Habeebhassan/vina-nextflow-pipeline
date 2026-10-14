# Start from a clean, lightweight Python environment
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required bioinformatics and chemistry libraries permanently
RUN pip install --default-timeout=1000 --no-cache-dir rdkit meeko gemmi numpy scipy
