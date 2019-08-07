from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps_dir.interview_calendar.models import Period, Reservation
from apps_dir.interview_calendar.serializers import (
    AvailableSlotsSerializer, PeriodSerializer, ReservationSerializer, InterviewScheduleSerializer
)
from utilities.utils import get_my_available_slots


class TeamAvailability(APIView):

    def all_users(self, serializer):
        """
        :param serializer: The validated serializer
        :return: The list of users as a flat list
        """
        list_of_users = []
        # get all the persons whose times must
        for item in serializer.data:
            if type(serializer.data[item]) == int:
                list_of_users.append(serializer.data[item])
            else:
                list_of_users += serializer.data[item]

        return list_of_users

    # todo: this really should be a GET request
    def post(self, request):
        """
        Get the times when an interview can be scheduled.
        Sample accepted data format:
        {
            "interviewers": [2],
            "candidate": 1
        }
        :param request:
        :return:
        """
        data = request.data
        # current_user = request.user
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        if available_slots_serializer.is_valid():

            list_of_users = self.all_users(available_slots_serializer)

            # get the slots for each one
            slots = [set(get_my_available_slots(user)) for user in list_of_users]

            # get the time that is common for all
            common_times = set.intersection(*slots)

            response = {
                "status": status.HTTP_200_OK,
                "content": {
                    "message": "success",
                    "available_times": sorted(common_times)
                }
            }
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "content": available_slots_serializer.errors
            }

        return Response(
            status=response["status"],
            data=response["content"],
            content_type="json"
        )

    def put(self, request):
        """
        Schedule an interview!
        :param request:
        :return:
        """

        interview_schedule_serializer = InterviewScheduleSerializer(data=request.data)

        if interview_schedule_serializer.is_valid():

            data = interview_schedule_serializer.data

            data["users"] = [
                interview_schedule_serializer.data["candidate"],
                *interview_schedule_serializer.data["interviewers"]
            ]

            actual_reservation_serializer = ReservationSerializer(data=data)
            # prevent duplicates

            if actual_reservation_serializer.is_valid():
                already_saved_reservations = Reservation.objects.filter(
                    users__in=data["users"],
                    start_time=interview_schedule_serializer.data["start_time"]
                )
                if not already_saved_reservations:
                    actual_reservation_serializer.save()
                    response = {
                        "status": status.HTTP_200_OK
                    }
                else:
                    response = {
                        "status": status.HTTP_409_CONFLICT
                    }
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "content": actual_reservation_serializer.errors
                }

        else:
            # todo: URGENT: This COULD be vulnerable to reflected xss
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "content": interview_schedule_serializer.errors,
            }
        return Response(
            status=response["status"],
            data=response.get("content")
        )


class IndividualAvailability(APIView):
    def get(self, request, target_user):
        """
        Get the slots when a particular individual is available for an individual

        :param request:
        :param current_user: This is the target user's id
        :return:
        """
        slots = get_my_available_slots(target_user)

        return Response(
            {
                "slots": slots,
                "count": len(slots)
            }
        )

    def post(self, request, target_user):
        """
        Add a when I have time
        :param request:
        :return:
        """
        # todo: Probably assert that target_user == request.user
        # i.e I'm the only one who can add my availability. But not a requirement at the moment
        data = {
            "start_time": request.data.get("start_time"),
            "end_time": request.data.get("end_time"),
            "user": target_user
        }
        period_serializer = PeriodSerializer(data=data)
        if period_serializer.is_valid():
            # todo: prevent overlapping times from being set
            # todo: prevent duplicates
            period_serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "content": "success"
            }
        else:
            # todo: this can be vulnerable
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "content": period_serializer.errors,
            }

        return Response(
            status=response["status"],
            data=response["content"]
        )

#
# class PeriodsViewSet(viewsets.ModelViewSet):
#     queryset = Period.objects.all()
#     serializer_class = PeriodSerializer
#
#
# class ReservationViewSet(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
