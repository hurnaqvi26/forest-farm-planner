from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from planner.auth_views import login_view, register_view, logout_view
from planner import views as planner_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    # Dashboard
    path("dashboard/", planner_views.dashboard, name="dashboard"),

    # Crop Yield Calculator
    path("calculator/", planner_views.crop_yield_calculator, name="crop_calculator"),
]


# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
