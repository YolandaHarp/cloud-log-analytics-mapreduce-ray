import sys
import csv


def main():
    reader = csv.DictReader(sys.stdin)

    for row in reader:
        service = row["service_name"].strip()
        status_code = int(row["status_code"])

        if status_code >= 500:
            print(f"{service}\t1")


if __name__ == "__main__":
    main()