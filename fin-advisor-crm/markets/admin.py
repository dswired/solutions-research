from django.contrib import admin
from .models import *

# Register your models here.
class DailyPublicEquityTradesAdmin(admin.ModelAdmin):
    list_display = [
        "trade_date",
        "ticker",
        "year_high",
        "year_low",
        "previous_closing_price",
        "opening_price",
        "last_transaction_price",
        "closing_price",
        "price_change",
        "closing_bid_price",
        "closing_offer_price",
        "total_shares_traded",
        "total_value_traded"
    ]
    search_fields = ["trade_date", "ticker"]
    ordering = ["trade_date", "ticker"]


admin.site.register(DailyPublicEquityTrades, DailyPublicEquityTradesAdmin)
