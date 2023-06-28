from django.contrib import admin

from example.models import Coin, CoinMarketData


class CoinMarketInlineAdmin(admin.TabularInline):
    model = CoinMarketData
    extra = 0


class CoinAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ["name", "symbol"]


class CoinMarketDataAdmin(admin.ModelAdmin):
    list_display = ("id", "coin", "date")
    list_display_links = ("id",)
    search_fields = ["coin__name", "date"]
    list_filter = ["coin", "date"]


admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinMarketData, CoinMarketDataAdmin)
