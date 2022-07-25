from typing import List

from config.error_codes import errors
from rest_framework import status
from rest_framework.exceptions import APIException

from django.conf import settings


class GenericException(APIException):
    """
    example:
    raise GenericException(error_code="user_001")
    """
    status_code = status.HTTP_400_BAD_REQUEST
    code = "default"
    message = ""
    show_message = settings.SHOW_ERROR_MESSAGE

    def __init__(self, error_code: str = None, status_code: int = None, message: str = None):
        self.code = error_code if error_code else "default"

        error_obj: List = errors.get(self.code, errors["default"])
        self.status_code, self.message = error_obj
        if status_code:
            self.status_code = status_code
        if message:
            self.message = message

        data = {
            "status": {
                "code": self.code,
            }
        }
        if self.show_message:
            data['status']['message'] = self.message

        super().__init__(data)


class StringReplaceException(GenericException):

    def __init__(self, code: str = None, string_value: str = ""):
        if code:
            self.code = code
        if self.code in errors.keys():
            self.message = str(errors[self.code][1])
        else:
            self.message = str(errors["default"][1])

        self.message = self.message.replace("[s]", string_value)
        super().__init__(error_code=self.code, message=self.message)
