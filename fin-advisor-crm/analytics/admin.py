from django.contrib import admin
from .models import *


# Register your models here.
class SecurityPriceAdmin(admin.ModelAdmin):
    list_display = ["securityid", "date", "price"]
    search_fields = ["securityid"]
    ordering = ["securityid", "date"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "security",
        "trade_date",
        "transaction_type",
        "transaction_quantity",
        "transaction_amount",
        "transaction_id",
    ]
    search_fields = ["account", "securityid", "transaction_type", "transaction_id"]
    ordering = ["account", "security", "trade_date"]


class PositionAdmin(admin.ModelAdmin):
    list_display = ["account", "security", "date", "quantity", "market_value"]
    search_fields = ["account", "security", "date"]
    ordering = ["account", "security", "date"]


class EntityTrendAdmin(admin.ModelAdmin):
    list_display = ["entity", "date", "total_portfolio_value"]
    search_fields = ["entity", "date"]
    ordering = ["entity", "date"]


admin.site.register(SecurityPrice, SecurityPriceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(EntityTrend, EntityTrendAdmin)
