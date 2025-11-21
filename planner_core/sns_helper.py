import boto3

TOPIC_ARN = "arn:aws:sns:us-east-1:675834675118:FarmPlanNotifications"


def notify_plan_created(plan_id, username):
    """
    Send SNS email notification when a farm plan is created.
    """
    sns = boto3.client("sns", region_name="us-east-1")

    message = (
        f"A new farm plan has been created.\n\n"
        f"Plan ID: {plan_id}\n"
        f"Created by: {username}\n"
    )

    subject = "🌱 New Farm Plan Created"

    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject=subject
    )

    print("SNS Email Notification Sent!")
