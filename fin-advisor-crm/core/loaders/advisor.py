from django.contrib.auth.models import User


def advisor(row: dict):
    User.objects.get_or_create(**row)
