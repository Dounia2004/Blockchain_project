from django.contrib import admin
from .models import Property, RentalContract

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'property_type', 'price_per_month', 'status', 'created_at']
    list_filter = ['property_type', 'status', 'city']
    search_fields = ['title', 'address', 'city']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'property_type', 'owner', 'status')
        }),
        ('Localisation', {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        ('Caractéristiques', {
            'fields': ('surface_area', 'rooms', 'bedrooms')
        }),
        ('Finances', {
            'fields': ('price_per_month', 'security_deposit')
        }),
        ('Blockchain', {
            'fields': ('blockchain_contract_address',),
            'classes': ('collapse',)
        }),
    )

@admin.register(RentalContract)
class RentalContractAdmin(admin.ModelAdmin):
    list_display = ['property', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'status']
    list_filter = ['status', 'start_date']
    search_fields = ['property__title', 'tenant__username']
    readonly_fields = ['id', 'created_at', 'blockchain_contract_address', 'blockchain_tx_hash']