from django.contrib import admin
from .models import EuropePost

class EuropePostAdmin(admin.ModelAdmin):
    list_display = ('location', 'arrival_date', 'date_posted')

admin.site.register(EuropePost, EuropePostAdmin)