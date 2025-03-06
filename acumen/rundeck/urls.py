from django.urls import path
from . import views

urlpatterns = [
    path("", views.rundeck_view, name="rundeck"),  # Load script execution UI
    path("execute-script/", views.stream_script_output, name="stream_script_output"),
    path("execution-logs/", views.execution_logs, name='execution_logs'),
]
