from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps_dir.interview_calendar.models import Period, Reservation
from apps_dir.interview_calendar.serializers import AvailableSlotsSerializer, PeriodSerializer, ReservationSerializer
from utilities.utils import get_my_available_slots


class InterviewCalendar(APIView):

    def post(self, request):
        data = request.data
        # current_user = request.user

        available_slots_serializer = AvailableSlotsSerializer(data=data)
        if available_slots_serializer.is_valid():

            list_of_users = []
            # get all the persons whose times must
            for item in available_slots_serializer.data:
                if type(available_slots_serializer.data[item]) == int:
                    list_of_users.append(available_slots_serializer.data[item])
                else:
                    list_of_users += available_slots_serializer.data[item]

            # get the slots for each one
            slots = [set(get_my_available_slots(user)) for user in list_of_users]

            # get the time that is common for all
            common_times = set.intersection(*slots)

            response = {
                "status": status.HTTP_200_OK,
                "content": {
                    "message": "success",
                    "list_of_users": list_of_users,
                    "slots": slots,
                    "common_times": sorted(common_times),
                    "len_common": len(common_times)
                }
            }
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "content": available_slots_serializer.errors
            }

        return Response(response)


class MyInterviewCalendar(APIView):
    def get(self, request, current_user):
        slots = get_my_available_slots(current_user)

        return Response(
            {
                "slots": slots,
                "count": len(slots)
            }
        )


class PeriodsViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer



class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
