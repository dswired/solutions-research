# Generated by Django 5.0.4 on 2024-06-03 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="entitytrend",
            options={"ordering": ["entity", "date"]},
        ),
    ]
