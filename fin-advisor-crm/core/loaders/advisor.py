from django.contrib.auth.models import User

# username=row["username"],
# password=row["password"],
# first_name=row["first_name"],
# last_name=row["last_name"],
# email=row["username"],
# is_active=row["is_active"],

def advisor(row: dict):
    User.objects.get_or_create(**row)
