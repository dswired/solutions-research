from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "clientid",
        "name",
        "client_type",
        "is_active",
        "date_opened",
        "advisor",
    ]
    search_fields = ["clientid", "advisor"]
    ordering = ["clientid"]


class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "accountid",
        "account_name",
        "clientid",
        "date_opened",
        "is_active",
    ]
    search_fields = ["accountid", "clientid"]
    ordering = ["accountid", "clientid"]


class SecurityIndustryAdmin(admin.ModelAdmin):
    search_fields = ["security_industry"]
    ordering = ["security_industry"]


class SecuritySectorAdmin(admin.ModelAdmin):
    search_fields = ["security_sector"]
    ordering = ["security_sector"]


class SecurityAdmin(admin.ModelAdmin):
    list_display = ["securityid", "name", "sector", "industry"]
    search_fields = ["securityid"]
    ordering = ["securityid"]


# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(SecuritySector, SecuritySectorAdmin)
admin.site.register(SecurityIndustry, SecurityIndustryAdmin)
admin.site.register(Security, SecurityAdmin)
