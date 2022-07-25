import os

from config.test_base import BaseTestCase


class TestGetPermissions(BaseTestCase):
    api_name = "account_operation_permission_list"
    path_to_folder = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "testcase/permissions"
    )
