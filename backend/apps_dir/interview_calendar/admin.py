from django.contrib import admin

# Register your models here.
from .models import Period

class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', "user", "start_time", "end_time", "duration", "time_left", )
    list_filter = ("start_time", "end_time", "user", )
    list_display_links = ('id', "duration", )
    search_fields = ("start_time", "end_time", )
    list_per_page = 10
    ordering = ("start_time", )

admin.site.register(Period, PeriodAdmin)