from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

# Core backend helpers
from planner_core.dynamo import save_plan
from planner_core.sqs_helper import send_plan_to_queue
from planner_core.sns_helper import notify_user_plan_created
from planner_core.cloudwatch_helper import (
    create_log_group,
    create_log_stream,
    put_log_event,
)

# Calculator library
from planner_core.crop_calculator import (
    Crop,
    YieldCalculator,
    SoilRecommender,
    WeatherAdjustment
)


# ---------------------------------------------------
# FARM DASHBOARD VIEW
# ---------------------------------------------------
@login_required
def dashboard(request):
    """
    Main farm planner dashboard.
    Handles:
    - plots_json input
    - DynamoDB save
    - SQS message
    - SNS email to user's registered email
    - CloudWatch log event
    """
    ctx = {}

    if request.method == "POST":
        raw_json = request.POST.get("plots_json", "[]")

        try:
            plots = json.loads(raw_json)
        except json.JSONDecodeError:
            plots = []

        # 1) Save plan in DynamoDB
        plan_id = save_plan(plots, request.user.username)

        # 2) Send SQS message
        send_plan_to_queue(plan_id, plots, request.user.username)

        # 3) Send SNS email ONLY to user's registered email
        user_email = (request.user.email or "").strip()
        if user_email:
            notify_user_plan_created(user_email, plan_id, request.user.username)
        else:
            print("[SNS] User has no email; skipping SNS.")

        # 4) CloudWatch Logs
        group_name = "FarmPlannerLogs"
        stream_name = request.user.username

        create_log_group(group_name)
        create_log_stream(group_name, stream_name)

        log_message = f"[PLAN_CREATED] user={request.user.username} plan_id={plan_id} plots={len(plots)}"
        put_log_event(group_name, stream_name, log_message)

        ctx["message"] = f"Plan created successfully! ID: {plan_id}"

    return render(request, "planner/dashboard.html", ctx)


# ---------------------------------------------------
# CROP YIELD CALCULATOR VIEW
# ---------------------------------------------------
@login_required
def crop_yield_calculator(request):
    """
    Uses custom Python calculation library to calculate:
    - total yield
    - weather-adjusted yield
    - profit
    - suitable crop recommendations
    """
    result = None
    recommendations = None

    if request.method == "POST":
        # Inputs
        crop_name = request.POST.get("crop_name")
        area_acres = float(request.POST.get("area"))
        yield_rate = float(request.POST.get("yield_rate"))
        price_per_kg = float(request.POST.get("price"))
        soil_type = request.POST.get("soil")
        weather = request.POST.get("weather")

        # Create crop model
        crop = Crop(
            name=crop_name,
            yield_rate=yield_rate,
            price_per_kg=price_per_kg
        )

        # Load calculators
        yc = YieldCalculator()
        wa = WeatherAdjustment()
        sr = SoilRecommender()

        # Perform calculations
        base_yield = yc.calculate_total_yield(area_acres, crop)
        adjusted_yield = wa.adjust_yield(base_yield, weather)
        profit = yc.calculate_profit(adjusted_yield, crop)
        recommendations = sr.get_recommendations(soil_type)

        # Output data
        result = {
            "crop_name": crop_name,
            "area": area_acres,
            "yield_rate": yield_rate,
            "base_yield": base_yield,
            "adjusted_yield": adjusted_yield,
            "price": price_per_kg,
            "total_profit": profit,
            "soil": soil_type,
            "weather": weather
        }

    return render(request, "planner/crop_calculator.html", {
        "result": result,
        "recommendations": recommendations
    })