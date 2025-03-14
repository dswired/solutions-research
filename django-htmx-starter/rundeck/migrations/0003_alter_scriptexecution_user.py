# Generated by Django 5.1.6 on 2025-03-06 03:35

import django.db.models.deletion
import rundeck.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rundeck", "0002_scriptexecution_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="scriptexecution",
            name="user",
            field=models.ForeignKey(
                default=rundeck.models.get_default_user,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
