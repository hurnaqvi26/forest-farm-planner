import boto3

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:675834675118:FarmPlanNotifications"


def get_subscription_status(user_email):
    """
    Check whether the user's email is subscribed, unsubscribed, or pending.
    Returns: "Confirmed", "PendingConfirmation", "NotFound"
    """

    sns = boto3.client("sns", region_name="us-east-1")
    response = sns.list_subscriptions_by_topic(TopicArn=SNS_TOPIC_ARN)

    for sub in response.get("Subscriptions", []):
        if sub["Endpoint"] == user_email:
            return sub["SubscriptionArn"]

    return "NotFound"


def subscribe_user_email(user_email):
    """
    Subscribe a user's email to SNS.
    The user must confirm via email.
    """
    sns = boto3.client("sns", region_name="us-east-1")

    sns.subscribe(
        TopicArn=SNS_TOPIC_ARN,
        Protocol="email",
        Endpoint=user_email
    )

    print(f"[SNS] Subscription requested for {user_email}. User must confirm.")
    return True


def notify_user_plan_created(user_email, plan_id, username):
    """
    Sends an SNS email ONLY if the user is fully subscribed.
    If not subscribed, auto-resubscribe and warn user.
    """

    subscription_arn = get_subscription_status(user_email)

    # 🟥 Not subscribed at all → auto-subscribe first
    if subscription_arn == "NotFound":
        print(f"[SNS] {user_email} is NOT subscribed. Re-subscribing...")
        subscribe_user_email(user_email)
        print("[SNS] Notification NOT sent (awaiting confirmation).")
        return

    # 🟡 Subscribed but not confirmed yet
    if subscription_arn == "PendingConfirmation":
        print(f"[SNS] Subscription for {user_email} is pending confirmation.")
        print("[SNS] User must confirm email before receiving notifications.")
        return

    # 🟢 Confirmed subscription → send the plan email
    sns = boto3.client("sns", region_name="us-east-1")

    message = (
        f"🌱 Your farm plan is ready!\n"
        f"User: {username}\n"
        f"Plan ID: {plan_id}\n\n"
        f"Thank you for using Farm Planner!"
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="🌾 Your Farm Plan Is Ready!"
    )

    print(f"[SNS] Email sent to {user_email}")
