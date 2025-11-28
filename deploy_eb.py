import boto3
import time
import zipfile
import os
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
APP_NAME = "ForestFarmPlanner"
ENV_NAME = "forest-farm-env"
S3_BUCKET = "eb-deploy-675834675118-us-east-1"
ZIP_FILE = "farmplanner.zip"


def wait_for_version_processed(eb, app_name, version_label):
    print(f"[WAIT] Waiting for application version '{version_label}' to finish processing...")

    while True:
        response = eb.describe_application_versions(
            ApplicationName=app_name,
            VersionLabels=[version_label]
        )

        status = response["ApplicationVersions"][0]["Status"]
        print(f"[INFO] Current status: {status}")

        if status == "Processed":
            print("[OK] Version processed successfully!")
            break

        time.sleep(5)


def main():
    print("=== Forest & Farm Planner • Elastic Beanstalk Deploy ===")

    if not os.path.exists(ZIP_FILE):
        print(f"[ERROR] ZIP file '{ZIP_FILE}' does not exist.")
        return

    print("[OK] Found deployment ZIP:", ZIP_FILE)

    s3 = boto3.client("s3", region_name=AWS_REGION)
    eb = boto3.client("elasticbeanstalk", region_name=AWS_REGION)

    # ------------------------------
    # Step 1: Ensure S3 bucket exists
    # ------------------------------
    try:
        s3.head_bucket(Bucket=S3_BUCKET)
        print("[OK] Bucket exists:", S3_BUCKET)
    except:
        print("[INFO] Creating S3 bucket:", S3_BUCKET)
        s3.create_bucket(
            Bucket=S3_BUCKET,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
        )
        print("[OK] Bucket created.")

    # ------------------------------
    # Step 2: Upload ZIP to S3
    # ------------------------------
    version_label = "ver-" + time.strftime("%Y%m%d-%H%M%S")
    s3_key = f"{version_label}.zip"

    print(f"[INFO] Uploading {ZIP_FILE} to S3 as {s3_key}...")
    s3.upload_file(ZIP_FILE, S3_BUCKET, s3_key)
    print("[OK] Upload complete.")

    # ------------------------------
    # Step 3: Create EB Application (if not exists)
    # ------------------------------
    try:
        eb.create_application(ApplicationName=APP_NAME, Description="Forest Farm Planner")
        print("[OK] EB Application created.")
    except ClientError as e:
        if "already exists" in str(e):
            print("[OK] EB Application already exists.")
        else:
            raise e

    # ------------------------------
    # Step 4: Create EB Application Version
    # ------------------------------
    print(f"[INFO] Creating application version {version_label}...")
    eb.create_application_version(
        ApplicationName=APP_NAME,
        VersionLabel=version_label,
        SourceBundle={
            "S3Bucket": S3_BUCKET,
            "S3Key": s3_key
        },
        Process=True  # IMPORTANT
    )
    print("[OK] Application version created.")

    # ------------------------------
    # Step 5: Wait for version to finish processing
    # ------------------------------
    wait_for_version_processed(eb, APP_NAME, version_label)

    # ------------------------------
    # Step 6: Create EB Environment
    # ------------------------------
    print(f"[INFO] Creating EB environment {ENV_NAME}...")

    try:
        eb.create_environment(
            ApplicationName=APP_NAME,
            EnvironmentName=ENV_NAME,
            VersionLabel=version_label,
            SolutionStackName="64bit Amazon Linux 2 v3.8.0 running Python 3.9",
        )
        print("[OK] Environment creation started!")

    except ClientError as e:
        if "already exists" in str(e):
            print("[WARN] Environment already exists. Updating instead...")

            eb.update_environment(
                EnvironmentName=ENV_NAME,
                VersionLabel=version_label
            )

            print("[OK] Environment updated.")
        else:
            raise e


if __name__ == "__main__":
    main()
