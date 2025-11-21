from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

from planner_core.dynamo import save_plan
from planner_core.sns_helper import notify_plan_created


@login_required
def dashboard(request):
    ctx = {}

    if request.method == "POST":
        raw = request.POST.get("plots_json", "[]")

        try:
            plots = json.loads(raw)
        except:
            plots = []

        # SAVE PLAN TO DYNAMODB
        plan_id = save_plan(plots, request.user.username)

        # SEND SNS EMAIL
        notify_plan_created(plan_id, request.user.username)

        ctx["message"] = f"Plan saved successfully! DynamoDB ID: {plan_id} (Email sent)"

    return render(request, "planner/dashboard.html", ctx)
