from django.contrib import admin
from .models import Ticker, TickerMetadata, HistoricalPrice

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'exchange')
    search_fields = ('symbol', 'name')
    list_filter = ('sector', 'industry')


@admin.register(TickerMetadata)
class TickerMetadataAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'last_updated', 'market_cap', 'beta')


@admin.register(HistoricalPrice)
class HistoricalPriceAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'date', 'close_price', 'volume')
    list_filter = ('ticker', 'date')