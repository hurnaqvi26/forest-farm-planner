import boto3
import logging
import os

logger = logging.getLogger(__name__)

BUCKET_NAME = "forest-farm-planner-storage"
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)


# ------------------------------------------------------
# Upload file for a user's plot
# ------------------------------------------------------
def upload_plot_image(file_path, username, plot_id):
    key = f"users/{username}/plots/{plot_id}.jpg"

    try:
        s3.upload_file(file_path, BUCKET_NAME, key)
        logger.info(f"Uploaded to S3: {key}")
        return key
    except Exception as e:
        logger.error(f"S3 UPLOAD ERROR: {e}")
        raise


# ------------------------------------------------------
# List all objects for a user
# ------------------------------------------------------
def list_user_objects(username):
    prefix = f"users/{username}/plots/"

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        contents = response.get("Contents", [])
        return [obj["Key"] for obj in contents]
    except Exception as e:
        logger.error(f"S3 LIST ERROR: {e}")
        return []


# ------------------------------------------------------
# Generate public URL for an object
# ------------------------------------------------------
def get_file_url(key):
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
