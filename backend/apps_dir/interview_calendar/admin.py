from django.contrib import admin

# Register your models here.
from apps_dir.interview_calendar.models import Period, Reservation


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', "user", "start_time", "end_time", "duration", "time_left",)
    list_filter = ("start_time", "end_time", "user",)
    list_display_links = ('id', "duration",)
    search_fields = ("start_time", "end_time",)
    list_per_page = 10
    ordering = ("start_time",)


admin.site.register(Period, PeriodAdmin)


class UsersInline(admin.TabularInline):
    extra = 0
    model = Reservation.users.through
    min_num = 2


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", 'id', "team", "start_time",)
    list_filter = ("start_time", "users",)
    list_display_links = ('id', "name",)
    search_fields = ("start_time", "name",)
    list_per_page = 10
    ordering = ("start_time",)
    inlines = (UsersInline,)


admin.site.register(Reservation, ReservationAdmin)
