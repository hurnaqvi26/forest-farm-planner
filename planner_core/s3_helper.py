import boto3
import logging
import os

logger = logging.getLogger(__name__)

# ================================================
#  S3 CONFIGURATION
# ================================================
BUCKET_NAME = "forest-farm-planner-storage"
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)


# ================================================
#  UPLOAD FARM IMAGE
#  /users/<username>/plots/<plot_id>.jpg
# ================================================
def upload_plot_image(file_path, username, plot_id):

    # Keep original extension (jpg, png, jpeg)
    ext = os.path.splitext(file_path)[-1].lower()
    if ext not in [".jpg", ".jpeg", ".png"]:
        ext = ".jpg"

    key = f"users/{username}/plots/{plot_id}{ext}"

    try:
        s3.upload_file(file_path, BUCKET_NAME, key)
        logger.info(f"Uploaded to S3: {key}")
        return key
    except Exception as e:
        logger.error(f"S3 UPLOAD ERROR: {e}")
        raise


# ================================================
#  LIST IMAGES FOR A USER
# ================================================
def list_user_objects(username):
    prefix = f"users/{username}/plots/"

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        if response.get("KeyCount", 0) == 0:
            return []

        return [obj["Key"] for obj in response.get("Contents", [])]

    except Exception as e:
        logger.error(f"S3 LIST ERROR: {e}")
        return []


# ================================================
#  GET PUBLIC URL FOR A FILE
# ================================================
def get_file_url(key):
    """Return the HTTPS public URL to access an S3 object."""
    return f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{key}"
