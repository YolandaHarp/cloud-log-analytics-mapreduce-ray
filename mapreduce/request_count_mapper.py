import sys
import csv


def main():
    reader = csv.DictReader(sys.stdin)

    for row in reader:
        service = row["service_name"].strip()
        print(f"{service}\t1")


if __name__ == "__main__":
    main()