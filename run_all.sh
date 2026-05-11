#!/bin/bash

set -e

DATASET="data/cloud_service_logs.csv"

mkdir -p outputs

echo "Running MapReduce Job 1: Request Count by Service"
time sh -c "cat $DATASET \
| python3 mapreduce/request_count_mapper.py \
| sort \
| python3 mapreduce/sum_reducer.py \
> outputs/request_count_by_service.txt"

echo "Running MapReduce Job 2: Server Error Count by Service"
time sh -c "cat $DATASET \
| python3 mapreduce/error_count_mapper.py \
| sort \
| python3 mapreduce/sum_reducer.py \
> outputs/server_error_count_by_service.txt"

echo "Running MapReduce Job 3: Top 10 Slow Endpoints"
time sh -c "cat $DATASET \
| python3 mapreduce/slow_endpoint_mapper.py \
| sort \
| python3 mapreduce/top10_reducer.py \
> outputs/top10_slow_endpoints.txt"

echo "Running Ray Degraded Service Detection"
time python3 ray/degraded_service_detection.py

echo "All tasks completed. Outputs are stored in outputs/."