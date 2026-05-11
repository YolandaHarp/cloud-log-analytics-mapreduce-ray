import argparse
import boto3


def upload_file_to_s3(local_file, bucket_name, object_key):
    s3 = boto3.client("s3")
    s3.upload_file(local_file, bucket_name, object_key)
    print(f"Uploaded {local_file} to s3://{bucket_name}/{object_key}")


def main():
    parser = argparse.ArgumentParser(description="Upload dataset to Amazon S3.")
    parser.add_argument("--local-file", required=True, help="Local dataset path")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--key", required=True, help="S3 object key")

    args = parser.parse_args()

    upload_file_to_s3(args.local_file, args.bucket, args.key)


if __name__ == "__main__":
    main()