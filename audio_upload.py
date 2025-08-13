import boto3
import os
from datetime import datetime, timezone

bucket = "apnearecordings"
patient_id = "patient001"
file_path = "text.txt"

timestamp = datetime.now(timezone.utc)
prefix = f"{patient_id}/{timestamp:%Y/%m/%d/%H/%M/%S}"
key = f"{prefix}/{os.path.basename(file_path)}"

s3 = boto3.client("s3")
s3.upload_file(Filename=file_path, Bucket=bucket, Key=key, ExtraArgs={"ServerSideEncryption": "AES256", "ContentType": "text/plain"})

print(f"Uploaded to s3://{bucket}/{key}")

