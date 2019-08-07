from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from apps_dir.interview_calendar.views import TeamAvailability, IndividualAvailability #, PeriodsViewSet, ReservationViewSet
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('periods', PeriodsViewSet)
# router.register('reservations', ReservationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    path('team_availability', TeamAvailability.as_view(), name="team_availability"),
    path('individual_availability/<int:target_user>', IndividualAvailability.as_view(), name="individual_availability"),
    path('accounts/', include('apps_dir.accounts.urls')),  # new
    path('token-auth/', obtain_jwt_token, name="token-auth")
]
