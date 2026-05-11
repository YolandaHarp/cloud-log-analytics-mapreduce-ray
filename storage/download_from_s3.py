import argparse
import boto3


def download_file_from_s3(bucket_name, object_key, local_file):
    s3 = boto3.client("s3")
    s3.download_file(bucket_name, object_key, local_file)
    print(f"Downloaded s3://{bucket_name}/{object_key} to {local_file}")


def main():
    parser = argparse.ArgumentParser(description="Download dataset from Amazon S3.")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--key", required=True, help="S3 object key")
    parser.add_argument("--local-file", required=True, help="Local output file path")

    args = parser.parse_args()

    download_file_from_s3(args.bucket, args.key, args.local_file)


if __name__ == "__main__":
    main()