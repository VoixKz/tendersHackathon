from django.contrib import admin
from .models import Tender, Offer

class TenderAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'start_date', 'end_date', 'created_by', 'created_at', 'blockchain_tx', 'tag', 'type')
    list_filter = ('created_by', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'created_by__email', 'blockchain_tx')

class OfferAdmin(admin.ModelAdmin):
    list_display = ('tender', 'contractor', 'price', 'created_at')
    list_filter = ('tender', 'contractor')
    search_fields = ('tender__title', 'contractor__email')

admin.site.register(Tender, TenderAdmin)
admin.site.register(Offer, OfferAdmin)
