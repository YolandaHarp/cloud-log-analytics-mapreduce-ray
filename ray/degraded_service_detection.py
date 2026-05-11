import csv
import time
from collections import defaultdict

import ray


DATASET_PATH = "data/cloud_service_logs.csv"
OUTPUT_PATH = "outputs/degraded_services.txt"
CHUNK_SIZE = 5000


def read_dataset_in_chunks(path, chunk_size):
    chunks = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        current_chunk = []

        for row in reader:
            current_chunk.append(row)

            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk)
                current_chunk = []

        if current_chunk:
            chunks.append(current_chunk)

    return chunks


@ray.remote
def process_chunk(rows):
    partial_stats = defaultdict(lambda: {
        "total": 0,
        "slow": 0,
        "server_error": 0,
        "timeout": 0
    })

    for row in rows:
        service = row["service_name"].strip()
        status_code = int(row["status_code"])
        response_time_ms = int(row["response_time_ms"])
        error_type = row.get("error_type", "").strip()

        partial_stats[service]["total"] += 1

        if response_time_ms > 800:
            partial_stats[service]["slow"] += 1

        if status_code >= 500:
            partial_stats[service]["server_error"] += 1

        if error_type == "Timeout":
            partial_stats[service]["timeout"] += 1

    return dict(partial_stats)


def combine_partial_results(partial_results):
    combined_stats = defaultdict(lambda: {
        "total": 0,
        "slow": 0,
        "server_error": 0,
        "timeout": 0
    })

    for partial in partial_results:
        for service, stats in partial.items():
            combined_stats[service]["total"] += stats["total"]
            combined_stats[service]["slow"] += stats["slow"]
            combined_stats[service]["server_error"] += stats["server_error"]
            combined_stats[service]["timeout"] += stats["timeout"]

    return combined_stats


def detect_degraded_services(combined_stats):
    degraded_services = []

    for service, stats in combined_stats.items():
        total = stats["total"]
        slow_rate = stats["slow"] / total
        server_error_rate = stats["server_error"] / total
        timeout_count = stats["timeout"]

        if slow_rate > 0.20:
            degraded_services.append((service, "high slow request rate"))

        if server_error_rate > 0.10:
            degraded_services.append((service, "high server error rate"))

        if timeout_count >= 5:
            degraded_services.append((service, "repeated timeout errors"))

    return degraded_services


def main():
    start_time = time.time()

    ray.init(ignore_reinit_error=True)

    chunks = read_dataset_in_chunks(DATASET_PATH, CHUNK_SIZE)

    futures = [
        process_chunk.remote(chunk)
        for chunk in chunks
    ]

    partial_results = ray.get(futures)

    combined_stats = combine_partial_results(partial_results)
    degraded_services = detect_degraded_services(combined_stats)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        for service, reason in degraded_services:
            line = f"{service},{reason}"
            print(line)
            file.write(line + "\n")

    end_time = time.time()
    print(f"Ray execution time: {end_time - start_time:.4f} seconds")

    ray.shutdown()


if __name__ == "__main__":
    main()
