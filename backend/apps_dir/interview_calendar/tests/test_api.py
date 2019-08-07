import json
from copy import deepcopy

import requests
from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.reverse import reverse

from apps_dir.accounts.models import User


class TestTeamAvailability(LiveServerTestCase):

    def get_users(self, user_type):
        user_types = {
            "interviewer": 2,
            "candidate": 3,
        }
        return [user.id for user in User.objects.filter(user_type=user_types[user_type])]

    def setUp(self):
        # Set up data for the whole TestCase
        super(TestTeamAvailability, self).setUp()

        self.users = [
            {
                "username": "john",
                "password": "H2pu1R961mx@KFtC$VkH",
                "user_type": "interviewer",
                "start_time": "2019-08-08T08:00:00",
                "end_time": "2019-08-09T17:00:00"
            },
            {
                "username": "mary",
                "password": "j7Y#VJGSV6Mde3k4em*1",
                "user_type": "interviewer",
                "start_time": "2019-08-08T11:00:00",
                "end_time": "2019-08-09T23:00:00"
            },
            {
                "username": "emmanuel",
                "password": "Q&x@K1OWG^6F1bjx%Yvv",
                "user_type": "candidate",
                "start_time": "2019-08-09T12:00:00",
                "end_time": "2019-08-10T23:00:00"
            },
        ]

        self.token = None

        for user in self.users:
            # test sign up
            response = self.client.post(
                path=f"{reverse('signup')}",
                data=user
            )
            self.assertTrue(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(type(response.data.get("token")), str)

            person = User.objects.get_by_natural_key(user["username"])
            # set up one as a candidate
            if user["user_type"] == "interviewer":
                person.user_type = 2
                person.save()

            user["user_id"] = person.id

            # test login
            response = self.client.post(
                path=f"{reverse('token-auth')}",
                data=user
            )

            # I know I'll only have the last one
            self.token = response.data.get("token")
            self.autorization = {
                "Authorization": f"JWT {self.token}"
            }

    def add_users_data(self):
        """
        Call this function to add test data
        This is also tests that
        "Individuals can add slots when they have time independently from each other"
        :return:
        """
        for user in self.users:
            response = requests.post(
                url=self.live_server_url + reverse(
                    'individual_availability',
                    kwargs={"target_user": user['user_id']})
                ,
                data=user,
                headers=self.autorization
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content), "success")

    def test_no_fields_provided(self):
        data = {}

        response = requests.post(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            json.loads(response.content),
            {
                "non_field_errors": [
                    "Either interviewers or a candidate must be provided"
                ]
            }
        )

    def test_all_fields_provided_no_available_slots(self):
        data = {
            "interviewers": [7, 6],
            "candidate": 1
        }
        response = requests.post(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )

        self.assertEqual(response.status_code, 200)
        # no data has been provided so we do not expect anythong to be there
        self.assertDictEqual(json.loads(response.content), {'available_times': [], 'message': 'success'})

    def test_all_fields_provided_some_available_slots(self):
        """
        This tests that
        Anyone can retrieve a collection of slots when interviews can take place.
        :return:
        """
        data = {
            "interviewers": self.get_users("interviewer"),
            "candidate": self.get_users("candidate")[0],
        }

        # first add the data!
        self.add_users_data()

        response = requests.post(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )
        self.assertEqual(response.status_code, 200)

        # no data has been provided so we do not expect anythong to be there
        self.assertDictEqual(
            json.loads(response.content),
            {
                'message': 'success',
                'available_times': [
                    '2019-08-09T12:00:00',
                    '2019-08-09T13:00:00',
                    '2019-08-09T14:00:00',
                    '2019-08-09T15:00:00',
                    '2019-08-09T16:00:00'
                ]
            }
        )

    def test_all_fields_provided_some_data_wrong_ids(self):
        """
        Basically, the users do not exist or no intersection
        :return:
        """
        data = {
            "interviewers": [4, 8],
            "candidate": 3
        }

        # first add the data!
        self.add_users_data()

        response = requests.post(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )

        self.assertEqual(response.status_code, 200)
        # no data has been provided so we do not expect anythong to be there
        self.assertDictEqual(json.loads(response.content), {'available_times': [], 'message': 'success'})

    def test_missing_fields_schedule_interview(self):
        """
        This tests that some valudation is done for the required fields
        :return:
        """
        data = {
            "interviewers": self.get_users("interviewer"),
            "candidate": self.get_users("candidate")[0],
            "name": "Interview with Emmanuel",
            "start_time": "2019-08-09T12:00:00"
        }

        # first add the data!
        self.add_users_data()

        for field in data:
            test_copy = deepcopy(data)
            del test_copy[field]

            response = requests.put(
                url=f"{self.live_server_url}{reverse('team_availability')}",
                data=test_copy,
                headers=self.autorization
            )

            # import pdb;pdb.set_trace()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_fields(self):
        """
        This tests that
        The API allows the caller to optionally define the candidate and optionally to define one or more interviewer.
        :return:
        """
        data = {
            "interviewers": self.get_users("interviewer"),
            "candidate": self.get_users("candidate")[0],
        }

        # first add the data!
        self.add_users_data()
        expected_slots = [
            {'message': 'success',
             'available_times': ['2019-08-09T12:00:00', '2019-08-09T13:00:00', '2019-08-09T14:00:00',
                                 '2019-08-09T15:00:00', '2019-08-09T16:00:00', '2019-08-09T17:00:00',
                                 '2019-08-09T18:00:00', '2019-08-09T19:00:00']},
            {'message': 'success',
             'available_times': ['2019-08-08T11:00:00', '2019-08-08T12:00:00', '2019-08-08T13:00:00',
                                 '2019-08-08T14:00:00', '2019-08-08T15:00:00', '2019-08-08T16:00:00',
                                 '2019-08-08T17:00:00', '2019-08-08T18:00:00', '2019-08-08T19:00:00',
                                 '2019-08-09T08:00:00', '2019-08-09T09:00:00', '2019-08-09T10:00:00',
                                 '2019-08-09T11:00:00', '2019-08-09T12:00:00', '2019-08-09T13:00:00',
                                 '2019-08-09T14:00:00', '2019-08-09T15:00:00', '2019-08-09T16:00:00']}

        ]
        for field in data:
            test_copy = deepcopy(data)
            del test_copy[field]

            response = requests.post(
                url=f"{self.live_server_url}{reverse('team_availability')}",
                data=test_copy,
                headers=self.autorization
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # each one has their availability
            self.assertTrue(json.loads(response.content) in expected_slots)

    def test_at_least_one_interviewer_required(self):
        """
        This tests that some valudation is done for the required fields
        :return:
        """
        data = {
            "interviewers": [],
            "candidate": 3,
            "name": "Interview with Emmanuel",
            "start_time": "2019-08-09T12:00:00"
        }

        # first add the data!
        self.add_users_data()

        response = requests.put(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )

        # import pdb;pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(json.loads(response.content), {"interviewers": ["This field is required."]})

    def test_successful_schedule_interview(self):
        """
        This tests that some valudation is done for the required fields
        :return:
        """
        data = {
            "interviewers": self.get_users("interviewer"),
            "candidate": self.get_users("candidate")[0],
            "name": "Interview with Emmanuel",
            "start_time": "2019-08-09T12:00:00"
        }

        # first add the data!
        self.add_users_data()

        response = requests.put(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # confirm that the availablke slots for the three has changed
        response = requests.post(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data={
                "interviewers": self.get_users("interviewer"),
                "candidate": self.get_users("candidate")[0],
            },
            headers=self.autorization
        )

        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(
            json.loads(response.content),
            {
                'message': 'success',
                'available_times': [
                    '2019-08-09T13:00:00',
                    '2019-08-09T14:00:00',
                    '2019-08-09T15:00:00',
                    '2019-08-09T16:00:00'
                ]
            }
        )

        # test for handling duplicates
        response = requests.put(
            url=f"{self.live_server_url}{reverse('team_availability')}",
            data=data,
            headers=self.autorization
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # of course you cannot add your availability twice.
        with self.assertRaises(AssertionError):
            self.add_users_data()
