from rest_framework import serializers


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
