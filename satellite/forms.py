from django import forms
from .models import Satellite, Command, TelemetryData


class SatelliteForm(forms.ModelForm):
    """Satellite registration form"""

    class Meta:
        model = Satellite
        fields = [
            "name", "satellite_id", "orbit_type",
            "status", "launched_at"
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: ALOS-4"
            }),
            "satellite_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: SAT-001"
            }),
            "orbit_type": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: LEO, GEO, SSO"
            }),
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
            "launched_at": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local"
            }),
        }


class CommandForm(forms.ModelForm):
    """Command send form"""

    class Meta:
        model = Command
        fields = [
            "satellite", "command_type", "command_code",
            "parameters", "operator"
        ]
        widgets = {
            "satellite": forms.Select(attrs={
                "class": "form-control"
            }),
            "command_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "command_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: CMD-ATT-001"
            }),
            "parameters": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Example: target_angle=45.0, duration=120"
            }),
            "operator": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Operator name"
            }),
        }


class TelemetryDataForm(forms.ModelForm):
    """Telemetry data input form"""

    class Meta:
        model = TelemetryData
        fields = [
            "satellite",
            "temperature_battery", "temperature_solar_panel",
            "temperature_payload",
            "voltage_bus", "current_bus", "power_generation",
            "attitude_roll", "attitude_pitch", "attitude_yaw",
            "health_status", "received_at"
        ]
        widgets = {
            "satellite": forms.Select(attrs={
                "class": "form-control"
            }),
            "temperature_battery": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.1"
            }),
            "temperature_solar_panel": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.1"
            }),
            "temperature_payload": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.1"
            }),
            "voltage_bus": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01"
            }),
            "current_bus": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01"
            }),
            "power_generation": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.1"
            }),
            "attitude_roll": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01"
            }),
            "attitude_pitch": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01"
            }),
            "attitude_yaw": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01"
            }),
            "health_status": forms.Select(attrs={
                "class": "form-control"
            }),
            "received_at": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local"
            }),
        }