from rest_framework import serializers

from apps_dir.interview_calendar.models import Period, Reservation


class AvailableSlotsSerializer(serializers.Serializer):
    candidate = serializers.IntegerField(required=False)
    interviewers = serializers.ListField(
        child=serializers.IntegerField(required=True),
        min_length=1,
        max_length=10,
        required=False)

    def validate(self, data):
        if not data.get('candidate') and not data.get('interviewers'):
            raise serializers.ValidationError("Either interviewers or a candidate must be provided")
        return data


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'