from django.contrib import admin
from django.urls import path
from planner.auth_views import login_view, register_view, logout_view
from planner.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
]
