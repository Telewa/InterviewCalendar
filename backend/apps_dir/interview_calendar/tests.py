from unittest import TestCase

from rest_framework.exceptions import ErrorDetail

from apps_dir.interview_calendar.serializers import AvailableSlotsSerializer


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

    def test_only_candidate_provided(self):
        data = {
            "candidate": 1
        }
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertEqual(available_slots_serializer.is_valid(), True)

    def test_only_interviewers_provided(self):
        data = {
            "interviewers": [7, 6],
        }
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertEqual(available_slots_serializer.is_valid(), True)

    def test_interviewers_must_be_a_list(self):
        data = {
            "interviewers": 6,
        }
        available_slots_serializer = AvailableSlotsSerializer(data=data)
        self.assertEqual(available_slots_serializer.is_valid(), False)
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
        self.assertEqual(available_slots_serializer.is_valid(), False)
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