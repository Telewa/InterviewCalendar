from copy import deepcopy
from unittest import TestCase

from rest_framework.exceptions import ErrorDetail

from apps_dir.interview_calendar.serializers import AvailableSlotsSerializer, InterviewScheduleSerializer


class TestAvailableSlotsSerializer(TestCase):

    def test_no_fields_provided(self):
        data = {}
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertEqual(available_slots_serializer.is_valid(), False)

    def test_all_fields_provided(self):
        data = {
            "interviewers": [7, 6],
            "candidate": 1
        }
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertEqual(available_slots_serializer.is_valid(), True)

    def test_missing_fields(self):
        data = {
            "interviewers": [7, 6],
            "candidate": 1
        }

        for field in data:
            test_copy = deepcopy(data)
            del test_copy[field]

            available_slots_serializer = AvailableSlotsSerializer(data=test_copy)
            self.assertTrue(available_slots_serializer.is_valid())

    def test_interviewers_must_be_a_list(self):
        data = {
            "interviewers": 6,
        }
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertFalse(available_slots_serializer.is_valid())
        self.assertDictEqual(
            available_slots_serializer.errors,
            {
                'interviewers': [
                    ErrorDetail(
                        string='Expected a list of items but got type "int".',
                        code='not_a_list'
                    )
                ]
            }
        )

    def test_at_least_one_interviewer_required(self):
        data = {
            "interviewers": [],
        }
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertFalse(available_slots_serializer.is_valid())
        self.assertDictEqual(
            available_slots_serializer.errors,
            {
                'interviewers': [
                    ErrorDetail(
                        string='Ensure this field has at least 1 elements.',
                        code='min_length'
                    )
                ]
            }
        )


class TestInterviewScheduleSerializer(TestCase):

    def test_no_fields_provided(self):
        data = {}
        available_slots_serializer = InterviewScheduleSerializer(data=data)
        self.assertEqual(available_slots_serializer.is_valid(), False)

    def test_all_fields_provided(self):
        data = {
            "interviewers": [7, 6],
            "candidate": 1,
            "name": "Interview with Emmanuel",
            "start_time": "2019-08-08T08:00:00",
        }
        available_slots_serializer = InterviewScheduleSerializer(data=data)
        self.assertTrue(available_slots_serializer.is_valid())

    def test_all_invalid_date(self):
        data = {
            "interviewers": [7, 6],
            "candidate": 1,
            "name": "Interview with Emmanuel",
            "start_time": "2019-08-08B08:00:00",
        }
        available_slots_serializer = InterviewScheduleSerializer(data=data)
        self.assertFalse(available_slots_serializer.is_valid())
        self.assertDictEqual(
            available_slots_serializer.errors,
            {
                'start_time': [
                    ErrorDetail(
                        string='Datetime has wrong format. '
                               'Use one of these formats instead: '
                               'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].',
                        code='invalid'
                    )
                ]
            }
        )

    def test_missing_fields(self):
        """
        If any field is missing, return invalid
        :return:
        """
        data = {
            "interviewers": [7, 6],
            "candidate": 1,
            "name": "Interview with Emmanuel",
            "start_time": "2019-08-08T08:00:00",
        }
        for field in data:
            test_copy = deepcopy(data)
            del test_copy[field]

            available_slots_serializer = InterviewScheduleSerializer(data=test_copy)
            self.assertFalse(available_slots_serializer.is_valid())
