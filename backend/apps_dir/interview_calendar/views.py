# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class InterviewCalendar(APIView):
    def get(self, request):
        return Response("Welcome!")
