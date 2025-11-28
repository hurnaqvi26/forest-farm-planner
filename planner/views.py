from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

# DynamoDB + AWS Services
from planner_core.dynamo import save_plan, get_all_plans
from planner_core.sqs_helper import send_plan_to_queue
from planner_core.sns_helper import notify_user_plan_created
from planner_core.cloudwatch_helper import create_log_group, create_log_stream, put_log_event
from planner_core.s3_helper import upload_plot_image, list_user_objects, get_file_url

# PyPI Crop Calculator Package
from cropcalc_pkg.crop_functions import (
    Crop,
    YieldCalculator,
    WeatherAdjustment,
    SoilRecommender
)
@login_required
def export_pdf(request):
    import json
    from django.http import HttpResponse
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4

    raw_json = request.POST.get("plots_json", "[]")

    try:
        plots = json.loads(raw_json)
    except:
        plots = []

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=farm_plan.pdf"

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 80, "🌱 Forest & Farm Planner - Exported Plan")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 110, f"User: {request.user.username}")

    y = height - 150

    # Headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Plot ID")
    p.drawString(150, y, "Area")
    p.drawString(250, y, "Soil")
    p.drawString(350, y, "Crop")

    y -= 25
    p.setFont("Helvetica", 11)

    for plot in plots:
        p.drawString(50, y, str(plot.get("plotId")))
        p.drawString(150, y, str(plot.get("area")))
        p.drawString(250, y, str(plot.get("soil")))
        p.drawString(350, y, str(plot.get("crop")))
        y -= 22

        if y < 60:
            p.showPage()
            y = height - 60

    p.showPage()
    p.save()
    return response



# ====================================================
#  S3 STORAGE PAGE — Upload Farm Images
# ====================================================
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

        # Save temp file
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb+") as temp:
            for chunk in uploaded_file.chunks():
                temp.write(chunk)

        # Upload to S3
        upload_plot_image(temp_path, username, plot_id)

        # Refresh list
        uploaded_keys = list_user_objects(username)
        file_urls = [get_file_url(k) for k in uploaded_keys]

    return render(request, "planner/s3_storage.html", {
        "files": zip(uploaded_keys, file_urls)
    })


# ====================================================
#  DASHBOARD — Requires at least 1 S3 Image
# ====================================================
@login_required
def dashboard(request):
    ctx = {}

    # Check existing S3 uploads FIRST
    username = request.user.username
    uploaded_files = list_user_objects(username)

    ctx["uploaded_count"] = len(uploaded_files)

    if request.method == "POST":

        # If NO image uploaded → DO NOT SAVE THE PLAN
        if len(uploaded_files) == 0:
            ctx["message"] = "⛔ You must upload at least ONE farm image before saving a plan!"
            return render(request, "planner/dashboard.html", ctx)

        raw_json = request.POST.get("plots_json", "[]")

        try:
            plots = json.loads(raw_json)
        except json.JSONDecodeError:
            plots = []

        # 1 — Save plan in DynamoDB
        plan_id = save_plan(plots, username)

        # 2 — Send plan to SQS
        send_plan_to_queue(plan_id, plots, username)

        # 3 — Send SNS email
        email = (request.user.email or "").strip()
        if email:
            notify_user_plan_created(email, plan_id, username)
        else:
            print("[SNS] No email found for user.")

        # 4 — CloudWatch logs
        group = "FarmPlannerLogs"
        stream = username
        create_log_group(group)
        create_log_stream(group, stream)
        put_log_event(group, stream, f"[PLAN_CREATED] user={username} plan={plan_id}")

        ctx["message"] = f"Plan created successfully! ID: {plan_id}"

    return render(request, "planner/dashboard.html", ctx)


# ====================================================
#  VIEW ALL SAVED PLANS
# ====================================================
@login_required
def view_plans(request):
    plans = get_all_plans()
    plans = sorted(plans, key=lambda x: x.get("created_at", ""), reverse=True)
    return render(request, "planner/plans_list.html", {"plans": plans})


# ====================================================
#  CROP YIELD CALCULATOR (PyPI)
# ====================================================
@login_required
def crop_yield_calculator(request):
    result = None
    recommendations = None

    if request.method == "POST":
        crop_name = request.POST.get("crop_name")
        area_acres = float(request.POST.get("area"))
        yield_rate = float(request.POST.get("yield_rate"))
        price_per_kg = float(request.POST.get("price"))
        soil_type = request.POST.get("soil")
        weather = request.POST.get("weather")

        crop = Crop(
            name=crop_name,
            yield_rate=yield_rate,
            price_per_kg=price_per_kg
        )

        yc = YieldCalculator()
        wa = WeatherAdjustment()
        sr = SoilRecommender()

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
