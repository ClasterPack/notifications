# import datetime
# from unittest.mock import patch
#
# import pytest
# from celery.exceptions import Retry
# from freezegun import freeze_time
# from tests.data_for_tests import good_clinets_data
#
# from distribution.models import Client, Distribution
# from distribution.tasks import send_notification
#
#
# class TestSendDistribution:
#     @patch('distribution.tasks.Distribution.notification')
#     def test_success(self, distribution_to_send):
#         freezer = freeze_time('2022-10-14 12:00:00')
#         freezer.start()
#         for client in good_clinets_data:
#             Client.objects.create(client)
#         distribution = Distribution.objects.create(
#             start_tome=datetime.datetime.now(),
#             end_time=datetime.datetime.now(),
#             filter_tag='vasya',
#             filter_operator_code='999',
#             message='test message',
#         )
#         send_notification(distribution)
