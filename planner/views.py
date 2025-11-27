from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

from planner_core.dynamo import save_plan, get_all_plans
from planner_core.sqs_helper import send_plan_to_queue
from planner_core.sns_helper import notify_user_plan_created
from planner_core.cloudwatch_helper import create_log_group, create_log_stream, put_log_event
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Crop Calculator (PyPI Package)
from cropcalc_pkg.crop_functions import (
    Crop,
    YieldCalculator,
    WeatherAdjustment,
    SoilRecommender
)

from django.views.decorators.csrf import csrf_exempt
from planner_core.s3_helper import upload_plot_image, list_user_objects, get_file_url


@login_required
def s3_storage(request):
    username = request.user.username
    uploaded_keys = list_user_objects(username)
    file_urls = [get_file_url(k) for k in uploaded_keys]

    if request.method == "POST":
        plot_id = request.POST.get("plot_id")
        uploaded_file = request.FILES.get("image_file")

        if not plot_id or not uploaded_file:
            return render(request, "planner/s3_storage.html", {
                "error": "Plot ID and Image required!",
                "files": zip(uploaded_keys, file_urls)
            })

        # save file temporarily
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb+") as temp:
            for chunk in uploaded_file.chunks():
                temp.write(chunk)

        # upload to S3
        upload_plot_image(temp_path, username, plot_id)

        uploaded_keys = list_user_objects(username)
        file_urls = [get_file_url(k) for k in uploaded_keys]

    return render(request, "planner/s3_storage.html", {
        "files": zip(uploaded_keys, file_urls)
    })


# ================================
#  DASHBOARD VIEW
# ================================
@login_required
def dashboard(request):
    ctx = {}

    if request.method == "POST":
        raw_json = request.POST.get("plots_json", "[]")

        try:
            plots = json.loads(raw_json)
        except json.JSONDecodeError:
            plots = []

        # 1 – Save plan
        plan_id = save_plan(plots, request.user.username)

        # 2 – Send to SQS
        send_plan_to_queue(plan_id, plots, request.user.username)

        # 3 – Notify user by SNS (only if user has email)
        email = (request.user.email or "").strip()
        if email:
            notify_user_plan_created(email, plan_id, request.user.username)
        else:
            print("[SNS] User has no email assigned. Skipping email.")

        # 4 – CloudWatch Logging
        group = "FarmPlannerLogs"
        stream = request.user.username
        create_log_group(group)
        create_log_stream(group, stream)

        log_message = f"[PLAN_CREATED] user={request.user.username} plan_id={plan_id} plots={len(plots)}"
        put_log_event(group, stream, log_message)

        ctx["message"] = f"Plan created successfully! ID: {plan_id}"

    return render(request, "planner/dashboard.html", ctx)



# ================================
#  VIEW ALL SAVED PLANS
# ================================
@login_required
def view_plans(request):
    plans = get_all_plans()

    # Sort newest first
    plans = sorted(plans, key=lambda x: x.get("created_at", ""), reverse=True)

    return render(request, "planner/plans_list.html", {"plans": plans})



# ================================
#  CROP YIELD CALCULATOR
# ================================
# @login_required
# def crop_yield_calculator(request):
#     """
#     Uses the published PyPI package:
#     cropcalc-hurnaqvi
#     """

#     result = None
#     recommendations = None

#     if request.method == "POST":
#         try:
#             crop_name = request.POST.get("crop_name")
#             area = float(request.POST.get("area"))
#             yield_rate = float(request.POST.get("yield_rate"))
#             price = float(request.POST.get("price"))
#             soil = request.POST.get("soil")
#             weather = request.POST.get("weather")

#             # Build Crop object
#             crop = Crop(
#                 name=crop_name,
#                 yield_rate=yield_rate,
#                 price_per_kg=price,
#             )

#             # Use PyPI library functionality
#             yc = YieldCalculator()
#             wa = WeatherAdjustment()
#             sr = SoilRecommender()

#             base_yield = yc.calculate_total_yield(area, crop)
#             adjusted_yield = wa.adjust_yield(base_yield, weather)
#             profit = yc.calculate_profit(adjusted_yield, crop)
#             recommendations = sr.get_recommendations(soil)

#             # Build result dictionary
#             result = {
#                 "crop_name": crop_name,
#                 "area": area,
#                 "yield_rate": yield_rate,
#                 "base_yield": base_yield,
#                 "adjusted_yield": adjusted_yield,
#                 "price": price,
#                 "profit": profit,
#                 "soil": soil,
#                 "weather": weather,
#             }

#         except Exception as e:
#             print("Calculator Error:", e)

#     return render(request, "planner/crop_calculator.html", {
#         "result": result,
#         "recommendations": recommendations
#     })
    


@login_required
def crop_yield_calculator(request):

    result = None
    recommendations = None

    if request.method == "POST":
        crop_name = request.POST.get("crop_name")
        area_acres = float(request.POST.get("area"))
        yield_rate = float(request.POST.get("yield_rate"))
        price_per_kg = float(request.POST.get("price"))   # <-- REQUIRED
        soil_type = request.POST.get("soil")
        weather = request.POST.get("weather")

        # Create Crop object (PyPI)
        crop = Crop(
            name=crop_name,
            yield_rate=yield_rate,
            price_per_kg=price_per_kg
        )

        yc = YieldCalculator()
        wa = WeatherAdjustment()
        sr = SoilRecommender()

        # Calculate values using your PyPI package
        base_yield = yc.calculate_total_yield(area_acres, crop)
        adjusted_yield = wa.adjust_yield(base_yield, weather)
        profit = yc.calculate_profit(adjusted_yield, crop)

        recommendations = sr.get_recommendations(soil_type)

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

