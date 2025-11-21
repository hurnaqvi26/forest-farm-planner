from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

# DynamoDB save function
from planner_core.dynamo import save_plan


@login_required
def dashboard(request):
    ctx = {}

    if request.method == "POST" and request.POST.get("plots_json"):
        raw_json = request.POST.get("plots_json", "[]")

        try:
            plots = json.loads(raw_json)
        except json.JSONDecodeError:
            plots = []

        # ------------- SAVE TO DYNAMODB -------------
        plan_id = save_plan(plots, request.user.username)

        ctx["message"] = f"Plan saved (DynamoDB active when AWS is ready). Plan ID: {plan_id}"

    return render(request, "planner/dashboard.html", ctx)
