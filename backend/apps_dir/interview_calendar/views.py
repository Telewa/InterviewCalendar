from rest_framework.response import Response
from rest_framework.views import APIView

from utilities.utils import get_my_slots


class InterviewCalendar(APIView):
    pass


class MyInterviewCalendar(APIView):
    def get(self, request):
        current_user = request.user

        slots = get_my_slots(current_user)

        return Response(
            {
                "slots": slots,
                "count": len(slots)
            }
        )
