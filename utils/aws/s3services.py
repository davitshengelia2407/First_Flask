import os
import boto3
from werkzeug.utils import secure_filename
from datetime import datetime, UTC


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file, folder="uploads"):
    if not file:
        raise ValueError("No file provided.")

    filename = secure_filename(file.filename)
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    key = f"{folder}/{timestamp}_{filename}"

    print(f"Uploading to S3 → Bucket: {S3_BUCKET_NAME} | Key: {key}")

    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME is not set in environment.")

    # ⛔️ Remove ACL since bucket doesn't support it
    s3.upload_fileobj(
        file,
        S3_BUCKET_NAME,
        key,
        ExtraArgs={"ContentType": file.content_type}
    )

    url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
    return url
