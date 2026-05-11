import sys


def main():
    counts = {}

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        key, value = line.split("\t")
        counts[key] = counts.get(key, 0) + int(value)

    top_10 = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    for key, count in top_10:
        print(f"{key}\t{count}")


if __name__ == "__main__":
    main()