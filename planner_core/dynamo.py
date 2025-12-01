import os
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
import boto3
from botocore.exceptions import ClientError

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMO_TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME", "FarmPlans")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE_NAME)


# ----------------------------------------------------
# Convert floats/strings recursively into Decimal
# ----------------------------------------------------
def convert_to_decimal(value):
    # Float → Decimal
    if isinstance(value, float):
        return Decimal(str(value))

    # Int → Decimal
    if isinstance(value, int):
        return Decimal(value)

    # Strings like "5" or "3.2" → Decimal
    if isinstance(value, str):
        try:
            return Decimal(value)
        except InvalidOperation:
            return value  # keep normal strings (soil, crop, etc.)

    # Dict → recursively clean
    if isinstance(value, dict):
        return {k: convert_to_decimal(v) for k, v in value.items()}

    # List → recursive clean
    if isinstance(value, list):
        return [convert_to_decimal(i) for i in value]

    return value


# ----------------------------------------------------
# SAVE PLAN (final, error-proof)
# ----------------------------------------------------
def save_plan(plots, username):

    # Convert everything to Decimal safely
    plots_clean = convert_to_decimal(plots)

    # Calculate total area (now safe)
    total_area = Decimal("0")
    for p in plots_clean:
        area = p.get("area", Decimal("0"))

        # After conversion, if still string → convert
        if isinstance(area, str):
            try:
                area = Decimal(area)
            except InvalidOperation:
                area = Decimal("0")

        total_area += area

    plan_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    # Build final DynamoDB item
    item = {
        "plan_id": plan_id,
        "username": username,
        "plots": plots_clean,
        "total_area": total_area,
        "created_at": created_at
    }

    try:
        table.put_item(Item=item)
        print("✔ Plan saved:", item)
    except ClientError as e:
        print("❌ DynamoDB Error:", e.response["Error"]["Message"])
        raise

    return plan_id


# ----------------------------------------------------
# GET plans
# ----------------------------------------------------
def get_all_plans():
    try:
        resp = table.scan()
        return resp.get("Items", [])
    except ClientError:
        return []