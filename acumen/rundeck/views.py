import os
import time
import datetime
import subprocess

from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import ScriptExecution


# TODO : Improve the UI for streamed logs?
#      : Allow filtering logs by execution status?
#      : Implement a frontend message when a script is killed due to timeout?
#      : Let users customize the timeout for each script?
#      : Add a "Stop Script" button to cancel execution?
#      : Format logs better (timestamps, colors, etc.)?
#      : Allow admins to view all user logs?
#      : Download logs as a CSV file?
#      : Allow UI selection of log levels instead of typing them manually?
#      : Ensure script execution updates the UI dynamically when it finishes?
#      : Show a "Running..." indicator when executing a script?
#      : How should I structure permissions for multi-user access in my Django app?


SCRIPTS_DIR = os.path.join(settings.BASE_DIR, "scripts")


def _get_ui_friendly_scriptname(filename: str) -> str:
    return filename.replace("_", " ").replace(".py", "").title()


def list_scripts():
    """Return a list of available scripts with user-friendly names, or raise an error if none exist."""

    if not os.path.isdir(SCRIPTS_DIR):
        raise FileNotFoundError(f"Scripts directory '{SCRIPTS_DIR}' not found!")

    script_files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py") and "utils" not in f]

    if not script_files:
        raise FileNotFoundError("No scripts found in the scripts directory!")

    # Return user-friendly names
    return [
        {"filename": f, "friendly_name": _get_ui_friendly_scriptname(f)}
        for f in script_files
    ]


@login_required
def rundeck_view(request):
    """Render the script execution page with user-friendly script names."""
    error_message = None  # Initialize error variable
    
    try:
        scripts = list_scripts()
        print(scripts)
    except FileNotFoundError as e:
        scripts = []
        error_message = str(e)  # Capture error

    return render(request, "rundeck/index.html", {"scripts": scripts, "error": error_message})



@login_required
def stream_script_output(request):
    """Stream script execution logs to the UI while saving logs to the database."""
    script_name = request.GET.get("script")
    arguments = request.GET.get("arguments", "").strip()

    if not script_name:
        return JsonResponse(
            {"output": "Error: No script selected", "success": False}, status=400
        )

    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.isfile(script_path):
        return JsonResponse(
            {
                "output": f"Error: Script '{script_name}' was not found.",
                "success": False,
            },
            status=400,
        )

    arg_list = arguments.split() if arguments else []
    start_time = datetime.datetime.now()
    logs = []  # Store logs for saving to database

    def stream():
        nonlocal logs  # Allows modification of 'logs' from the outer function

        try:
            process = subprocess.Popen(
                ["python3", script_path] + arg_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            for line in iter(process.stdout.readline, ""):
                logs.append(line.strip())  # Store logs for DB
                yield f"data: {line.strip()}\n\n"

            process.stdout.close()
            process.wait()

        except Exception as e:
            error_message = f"Unexpected Execution Error: {str(e)}"
            logs.append(error_message)
            yield f"data: {error_message}\n\n"

    response = StreamingHttpResponse(stream(), content_type="text/event-stream")

    # Save logs to the database once execution completes
    duration = datetime.datetime.now() - start_time
    ScriptExecution.objects.create(
        user=request.user,
        script_name=script_name,
        arguments=arguments,
        output="\n".join(logs),
        success=True if logs and "Error" not in logs[-1] else False,
        duration=duration,
    )

    return response


@login_required
def execution_logs(request):
    """Show past script execution logs."""
    logs = ScriptExecution.objects.filter(user=request.user).order_by("-timestamp")[
        :20
    ]  # Show last 20 logs per user
    return render(request, "rundeck/logs.html", {"logs": logs})
