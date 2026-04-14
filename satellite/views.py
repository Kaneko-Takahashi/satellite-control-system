from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Satellite, Command, TelemetryData
from .forms import SatelliteForm, CommandForm, TelemetryDataForm


# ============================================
# Dashboard
# ============================================
def dashboard(request):
    """Top page: show system overview"""
    context = {
        "satellites": Satellite.objects.all(),
        "total_satellites": Satellite.objects.count(),
        "total_commands": Command.objects.count(),
        "pending_commands": Command.objects.filter(status="pending").count(),
        "total_telemetry": TelemetryData.objects.count(),
        "recent_commands": Command.objects.all()[:5],
        "recent_telemetry": TelemetryData.objects.all()[:5],
    }
    return render(request, "satellite/dashboard.html", context)


# ============================================
# Satellite CRUD
# ============================================
def satellite_list(request):
    """Satellite list (Read)"""
    satellites = Satellite.objects.all()
    return render(request, "satellite/satellite_list.html", {
        "satellites": satellites
    })


def satellite_create(request):
    """Satellite registration (Create)"""
    if request.method == "POST":
        form = SatelliteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Satellite registered successfully.")
            return redirect("satellite:satellite_list")
    else:
        form = SatelliteForm()
    return render(request, "satellite/satellite_form.html", {
        "form": form,
        "title": "Register Satellite"
    })


def satellite_update(request, pk):
    """Satellite edit (Update)"""
    satellite = get_object_or_404(Satellite, pk=pk)
    if request.method == "POST":
        form = SatelliteForm(request.POST, instance=satellite)
        if form.is_valid():
            form.save()
            messages.success(request, "Satellite updated successfully.")
            return redirect("satellite:satellite_list")
    else:
        form = SatelliteForm(instance=satellite)
    return render(request, "satellite/satellite_form.html", {
        "form": form,
        "title": "Edit Satellite"
    })


def satellite_delete(request, pk):
    """Satellite delete (Delete)"""
    satellite = get_object_or_404(Satellite, pk=pk)
    if request.method == "POST":
        satellite.delete()
        messages.success(request, "Satellite deleted successfully.")
        return redirect("satellite:satellite_list")
    return render(request, "satellite/satellite_confirm_delete.html", {
        "object": satellite,
        "type_name": "Satellite"
    })


# ============================================
# Command CRUD
# ============================================
def command_list(request):
    """Command list (Read)"""
    commands = Command.objects.select_related("satellite").all()
    return render(request, "satellite/command_list.html", {
        "commands": commands
    })


def command_create(request):
    """Command create and send (Create)"""
    if request.method == "POST":
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save()
            messages.success(
                request,
                f"Command [{command.command_code}] created."
            )
            return redirect("satellite:command_list")
    else:
        form = CommandForm()
    return render(request, "satellite/command_form.html", {
        "form": form,
        "title": "Send Command"
    })


def command_detail(request, pk):
    """Command detail (Read)"""
    command = get_object_or_404(Command, pk=pk)
    return render(request, "satellite/command_detail.html", {
        "command": command
    })


def command_send(request, pk):
    """Execute command send"""
    command = get_object_or_404(Command, pk=pk)
    if command.status == "pending":
        command.send()
        messages.success(
            request,
            f"Command [{command.command_code}] sent."
        )
    else:
        messages.warning(request, "This command has already been processed.")
    return redirect("satellite:command_detail", pk=pk)


def command_update(request, pk):
    """Command edit (Update)"""
    command = get_object_or_404(Command, pk=pk)
    if request.method == "POST":
        form = CommandForm(request.POST, instance=command)
        if form.is_valid():
            form.save()
            messages.success(request, "Command updated successfully.")
            return redirect("satellite:command_list")
    else:
        form = CommandForm(instance=command)
    return render(request, "satellite/command_form.html", {
        "form": form,
        "title": "Edit Command"
    })


def command_delete(request, pk):
    """Command delete (Delete)"""
    command = get_object_or_404(Command, pk=pk)
    if request.method == "POST":
        command.delete()
        messages.success(request, "Command deleted successfully.")
        return redirect("satellite:command_list")
    return render(request, "satellite/satellite_confirm_delete.html", {
        "object": command,
        "type_name": "Command"
    })


# ============================================
# Telemetry CRUD
# ============================================
def telemetry_list(request):
    """Telemetry list (Read)"""
    telemetry = TelemetryData.objects.select_related("satellite").all()
    return render(request, "satellite/telemetry_list.html", {
        "telemetry_list": telemetry
    })


def telemetry_detail(request, pk):
    """Telemetry detail (Read)"""
    telemetry = get_object_or_404(TelemetryData, pk=pk)
    return render(request, "satellite/telemetry_detail.html", {
        "telemetry": telemetry
    })


def telemetry_create(request):
    """Telemetry data input (Create)"""
    if request.method == "POST":
        form = TelemetryDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Telemetry data registered.")
            return redirect("satellite:telemetry_list")
    else:
        form = TelemetryDataForm()
    return render(request, "satellite/telemetry_form.html", {
        "form": form,
        "title": "Register Telemetry Data"
    })


def telemetry_delete(request, pk):
    """Telemetry delete (Delete)"""
    telemetry = get_object_or_404(TelemetryData, pk=pk)
    if request.method == "POST":
        telemetry.delete()
        messages.success(request, "Telemetry data deleted.")
        return redirect("satellite:telemetry_list")
    return render(request, "satellite/satellite_confirm_delete.html", {
        "object": telemetry,
        "type_name": "Telemetry Data"
    })