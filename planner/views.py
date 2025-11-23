from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

from planner_core.dynamo import save_plan
from planner_core.sqs_helper import send_plan_to_queue
from planner_core.sns_helper import notify_user_plan_created
from planner_core.cloudwatch_helper import (
    create_log_group,
    create_log_stream,
    put_log_event,
)


@login_required
def dashboard(request):
    """
    Main farm planner dashboard:
    - Accepts plots_json from the frontend (JS)
    - Saves plan into DynamoDB
    - Sends plan message to SQS
    - Sends SNS email to the logged-in user (if email exists)
    - Writes log entry into CloudWatch Logs
    """
    ctx = {}

    if request.method == "POST":
        raw_json = request.POST.get("plots_json", "[]")

        try:
            plots = json.loads(raw_json)
        except json.JSONDecodeError:
            plots = []

        # 1) Save plan into DynamoDB
        plan_id = save_plan(plots, request.user.username)

        # 2) Send message to SQS queue
        send_plan_to_queue(plan_id, plots, request.user.username)

        # 3) Send SNS email to THIS user's email (if set)
        user_email = (request.user.email or "").strip()
        if user_email:
            notify_user_plan_created(user_email, plan_id, request.user.username)
        else:
            print("[SNS] User has no email; skipping SNS notification.")

        # 4) CloudWatch Logs - one group, stream per user
        group_name = "FarmPlannerLogs"
        stream_name = request.user.username  # e.g. "hurnaqvi"

        create_log_group(group_name)
        create_log_stream(group_name, stream_name)

        log_message = (
            f"[PLAN_CREATED] user={request.user.username} "
            f"plan_id={plan_id} plots_count={len(plots)}"
        )
        put_log_event(group_name, stream_name, log_message)

        # Message for template
        ctx["message"] = f"Plan created successfully! ID: {plan_id}"

    return render(request, "planner/dashboard.html", ctx)
