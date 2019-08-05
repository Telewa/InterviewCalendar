# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps_dir.accounts.models import User
from apps_dir.interview_calendar.models import Period


class InterviewCalendar(APIView):
    def get(self, request):
        interview_duration = 30
        candidate = User.objects.get_by_natural_key("emma")
        interviewer = User.objects.get_by_natural_key("teacher")

        Ia = Period.objects.get(id = 1, user=candidate)
        Ib = Period.objects.get(id = 2, user=interviewer)

        possible_start = max(Ia.start_time, Ib.start_time)
        # but the start can only be on top of the hour. So round up

        possible_end = min(Ia.end_time, Ib.end_time)
        max_duration = possible_end - possible_start

        return Response({
            interview_duration: interview_duration,
            "candidate": candidate.username,
            "interviewer": interviewer.username,
            "Ias": Ia.start_time,
            "Iae": Ia.end_time,
            "Ibs": Ib.start_time,
            "Ibe": Ib.end_time,
            "possible_start_time": possible_start,
            "possible_end_time": possible_end,
            "max_length": str(max_duration),
            "max_slots": (max_duration/60)/interview_duration
        })
