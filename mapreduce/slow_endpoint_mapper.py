import sys
import csv


def main():
    reader = csv.DictReader(sys.stdin)

    for row in reader:
        service = row["service_name"].strip()
        endpoint = row["endpoint"].strip()
        response_time_ms = int(row["response_time_ms"])

        if response_time_ms > 800:
            key = f"{service},{endpoint}"
            print(f"{key}\t1")


if __name__ == "__main__":
    main()