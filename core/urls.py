from django.contrib import admin
from django.urls import path
from planner import views as planner_views
from planner.auth_views import login_view, register_view, logout_view

urlpatterns = [

    # Auth
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    # Dashboard
    path("dashboard/", planner_views.dashboard, name="dashboard"),

    # Crop Calculator (this was missing!)
    path("calculator/", planner_views.crop_yield_calculator, name="crop_calculator"),

    # View All Saved Plans
    path("plans/", planner_views.view_plans, name="view_plans"),
    
    # S3 Bucket
    path("s3/", planner_views.s3_storage, name="s3_storage"),
    
    #Export PDF
    path("export-pdf/", planner_views.export_pdf, name="export_pdf"),
]