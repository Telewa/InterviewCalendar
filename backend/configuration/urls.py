from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from apps_dir.interview_calendar.views import InterviewCalendar, MyInterviewCalendar, PeriodsViewSet, ReservationViewSet
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

router = routers.DefaultRouter()
router.register('periods', PeriodsViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    path('schedule', InterviewCalendar.as_view(), name="schedule"),
    path('individual_slots/<int:current_user>', MyInterviewCalendar.as_view(), name="my_slots"),
    path('accounts/', include('apps_dir.accounts.urls')),  # new
    path('token-auth/', obtain_jwt_token)
]
