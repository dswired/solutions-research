from django.contrib import admin
from .models import *


# Register your models here.
class FakeAdressAdmin(admin.ModelAdmin):
    list_display = ["address"]
    search_fields = ["address"]


admin.site.register(FakeAdress, FakeAdressAdmin)
