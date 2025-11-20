from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json


@login_required
def dashboard(request):
    ctx = {}

    if request.method == "POST" and request.POST.get("plots_json"):
        raw_json = request.POST.get("plots_json", "[]")
        try:
            plots = json.loads(raw_json)
        except json.JSONDecodeError:
            plots = []

        # For now we don't save to AWS, just show a message.
        ctx["message"] = f"Plan received with {len(plots)} plots. (AWS disabled for now.)"

    return render(request, "planner/dashboard.html", ctx)
