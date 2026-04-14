from django.urls import path
from . import views

app_name = "satellite"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Satellite CRUD
    path("satellites/", views.satellite_list, name="satellite_list"),
    path("satellites/create/", views.satellite_create, name="satellite_create"),
    path("satellites/<int:pk>/edit/", views.satellite_update, name="satellite_update"),
    path("satellites/<int:pk>/delete/", views.satellite_delete, name="satellite_delete"),

    # Command CRUD
    path("commands/", views.command_list, name="command_list"),
    path("commands/create/", views.command_create, name="command_create"),
    path("commands/<int:pk>/", views.command_detail, name="command_detail"),
    path("commands/<int:pk>/send/", views.command_send, name="command_send"),
    path("commands/<int:pk>/edit/", views.command_update, name="command_update"),
    path("commands/<int:pk>/delete/", views.command_delete, name="command_delete"),

    # Telemetry CRUD
    path("telemetry/", views.telemetry_list, name="telemetry_list"),
    path("telemetry/create/", views.telemetry_create, name="telemetry_create"),
    path("telemetry/<int:pk>/", views.telemetry_detail, name="telemetry_detail"),
    path("telemetry/<int:pk>/delete/", views.telemetry_delete, name="telemetry_delete"),
]