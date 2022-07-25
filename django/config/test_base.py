import json
import os
from typing import Dict, List

from config import settings
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    """
    using by Inheritance this base class
    declare again the api_name, testcase_file and path_to_folder
    - testcases is the list of testcase using for this test, make it empty if using all file in path_to_folder
    (the list of fail testcases can be found at "All fail test" value when run unit test)
    - path_to_folder must re re declare in child class(can using same value as this class)
    """

    api_name = "base test"
    testcases: List[Dict[str, str]] = []
    path_to_folder = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "testcase"
    )

    def setUp(self):
        is_cognito_config_not_set = len(settings.COGNITO_USER_POOL) < 10 or len(settings.COGNITO_CLIENT_ID) < 10
        is_user_test_not_set = len(settings.TEST_COGNITO_USER_EMAIL) < 5 or len(settings.TEST_COGNITO_USER_PASSWORD) < 5

        if is_cognito_config_not_set or is_user_test_not_set:
            self.skipTest('Skip Cognito auth testcases since the settings are not set')

        self.set_client_auth()
        self.testcase_files = []
        self.case_ids = []
        for item in self.testcases:
            self.testcase_files.extend(item.keys())
            self.case_ids.extend(item.values())

    def test_api_testcase_file(self):

        list_error = []
        number_testcase = 0
        number_error = 0
        print("-------------------------------------------------------------")
        files = os.listdir(self.path_to_folder)
        if self.path_to_folder:
            for file in files:
                if not self.testcase_files or file in self.testcase_files:
                    path = os.path.join(self.path_to_folder, file)
                    with open(path, encoding="utf8") as data_file:
                        data = json.load(data_file)
                    for test_case in data:
                        if not self.case_ids or test_case["id"] in self.case_ids:
                            number_testcase += 1
                            testcase_id = test_case["id"]
                            url = test_case["url"]
                            name = test_case["name"]
                            params = test_case["params"]
                            if params:
                                url = url + '?'
                                for k, v in params.items():
                                    url = url + f'{k}={v}&'
                                url = url[:-1]
                            body = test_case["body"]
                            result = test_case["result"]
                            method = test_case["method"]
                            status = test_case["status_code"]
                            if method == "GET":
                                request = self.client.get(url, data=body)
                            elif method == "POST":
                                request = self.client.post(url, data=body)
                            elif method == "PUT":
                                request = self.client.put(url, data=body)
                            elif method == "DELETE":
                                request = self.client.delete(url, data=body)
                            try:
                                self.assertEqual(request.status_code, status)
                                if request.status_code != 404:
                                    response = json.loads(
                                        json.dumps(request.data))
                                    if isinstance(result, dict):
                                        self.compare_dict(result, response)
                                    elif isinstance(result, list):
                                        self.compare_list(result, response)
                                    else:
                                        self.assertEqual(result, response)
                            except Exception as e:
                                number_error = number_error + 1
                                error = {file: testcase_id}
                                list_error.append(error)
                                print("FILE NAME:", file)
                                print("FAIL TEST CASE:", name)
                                print(e)
                    print("------------")
        print("TEST RESULT FOR API NAME:", self.api_name)
        print("NUMBER OF TEST CASE:", number_testcase)
        print("NUMBER OF FAIL TEST:", number_error)
        print("ALL FAIL TEST:", list_error)
        self.assertEqual(number_error, 0)

    def compare_dict(self, except_result, response):
        self.assertEqual(type(except_result), type(response), "TYPE IS NOT VALID => " + str(except_result))
        for key, value in except_result.items():
            if type(value) is dict:
                self.compare_dict(value, response[key])
            elif type(value) is list:
                self.compare_list(value, response[key])
            else:
                self.assertIn(key, response)
                self.assertEqual([key, response[key]], [key, value])

    def compare_list(self, except_result, response):
        self.assertEqual(type(except_result), type(response), "TYPE IS NOT VALID => " + str(except_result))
        self.assertEqual(len(except_result), len(response),
                         "LENGTH OF LIST IS NOT RIGHT =>" + str(except_result) + "!= " + str(response))
        for i in range(len(except_result)):
            if type(except_result[i]) is dict:
                self.compare_dict(except_result[i], response[i])
            elif type(except_result[i]) is list:
                self.compare_list(except_result[i], response[i])
            else:
                self.assertEqual(response[i], except_result[i])

    def set_client_auth(self):
        login_body = {
            "email": settings.TEST_COGNITO_USER_EMAIL,
            "login_password": settings.TEST_COGNITO_USER_PASSWORD,
            "send_email_flag": True
        }
        login_url = "/console/api/v1/auth/token/"
        login_response = self.client.post(login_url, data=login_body)

        self.assertEqual(login_response.status_code, 200)
        data = login_response.data
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + data["token"])
