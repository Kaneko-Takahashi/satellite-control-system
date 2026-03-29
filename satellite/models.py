from django.db import models
from django.utils import timezone


class Satellite(models.Model):
    """Satellite basic info"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("standby", "Standby"),
        ("maintenance", "Maintenance"),
        ("decommissioned", "Decommissioned"),
    ]

    name = models.CharField(max_length=100)
    satellite_id = models.CharField(max_length=20, unique=True)
    orbit_type = models.CharField(max_length=50, default="LEO")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="standby"
    )
    launched_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.satellite_id})"


class Command(models.Model):
    """Command sent to satellite"""

    COMMAND_TYPE_CHOICES = [
        ("attitude", "Attitude Control"),
        ("power", "Power Control"),
        ("thermal", "Thermal Control"),
        ("payload", "Payload Operation"),
        ("communication", "Communication"),
        ("orbit", "Orbit Control"),
        ("maintenance", "Maintenance"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("acknowledged", "Acknowledged"),
        ("executed", "Executed"),
        ("failed", "Failed"),
    ]

    satellite = models.ForeignKey(
        Satellite, on_delete=models.CASCADE, related_name="commands"
    )
    command_type = models.CharField(
        max_length=20, choices=COMMAND_TYPE_CHOICES
    )
    command_code = models.CharField(max_length=50)
    parameters = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    operator = models.CharField(max_length=100)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_command_type_display()}] {self.command_code}"

    def send(self):
        self.status = "sent"
        self.sent_at = timezone.now()
        self.save()


class TelemetryData(models.Model):
    """Telemetry data received from satellite"""

    HEALTH_STATUS_CHOICES = [
        ("nominal", "Nominal"),
        ("warning", "Warning"),
        ("critical", "Critical"),
    ]

    satellite = models.ForeignKey(
        Satellite, on_delete=models.CASCADE, related_name="telemetry_data"
    )
    # Temperature
    temperature_battery = models.FloatField()
    temperature_solar_panel = models.FloatField()
    temperature_payload = models.FloatField()
    # Power
    voltage_bus = models.FloatField()
    current_bus = models.FloatField()
    power_generation = models.FloatField()
    # Attitude
    attitude_roll = models.FloatField(default=0.0)
    attitude_pitch = models.FloatField(default=0.0)
    attitude_yaw = models.FloatField(default=0.0)
    # Status
    health_status = models.CharField(
        max_length=20, choices=HEALTH_STATUS_CHOICES, default="nominal"
    )
    received_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-received_at"]

    def __str__(self):
        return f"{self.satellite.name} - {self.received_at:%Y-%m-%d %H:%M:%S}"

    @property
    def power_consumption(self):
        return round(self.voltage_bus * self.current_bus, 2)
