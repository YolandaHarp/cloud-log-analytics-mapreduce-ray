# Mini-Project 2: Cloud Service Log Analytics

## Project Overview

This project analyses a synthetic cloud service log dataset using cloud object storage, MapReduce-style Python scripts, and Ray-based parallel analytics.

Workflow:

cloud service log dataset → Amazon S3 → EC2 execution environment → MapReduce baseline analytics → Ray degraded-service detection → comparison

## Project Structure

- `storage/`: scripts for uploading and downloading the dataset from Amazon S3
- `mapreduce/`: mapper and reducer scripts for baseline analytics
- `ray/`: Ray-based degraded-service detection script
- `outputs/`: generated analytics outputs
- `run_all.sh`: script for running the full pipeline
- `requirements.txt`: Python dependencies

## Requirements

```bash
pip install -r requirements.txt