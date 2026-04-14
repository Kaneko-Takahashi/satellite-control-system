from django.contrib import admin
from .models import Satellite, Command, TelemetryData


@admin.register(Satellite)
class SatelliteAdmin(admin.ModelAdmin):
    list_display = [
        "name", "satellite_id", "orbit_type",
        "status", "launched_at", "created_at"
    ]
    list_filter = ["status", "orbit_type"]
    search_fields = ["name", "satellite_id"]


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = [
        "command_code", "satellite", "command_type",
        "status", "operator", "created_at", "sent_at"
    ]
    list_filter = ["status", "command_type"]
    search_fields = ["command_code", "operator"]


@admin.register(TelemetryData)
class TelemetryDataAdmin(admin.ModelAdmin):
    list_display = [
        "satellite", "temperature_battery", "voltage_bus",
        "power_generation", "health_status", "received_at"
    ]
    list_filter = ["health_status", "satellite"]
    search_fields = ["satellite__name"]
