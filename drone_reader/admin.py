from django.contrib import admin
from .models import QRCodeData

@admin.register(QRCodeData)
class QRCodeDataAdmin(admin.ModelAdmin):
    list_display = ('qr_data', 'title', 'code', 'timestamp', 'is_processed', 'product')
    list_filter = ('is_processed', 'timestamp')
    search_fields = ('qr_data', 'title', 'code')
    readonly_fields = ('timestamp',)
