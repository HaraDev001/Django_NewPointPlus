"""
CS-New Point Plus  Middleware
"""

import logging
import time
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

api_logger = logging.getLogger("api")


class PointPlusMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.extra = dict()

    def handle_5xx(self, response, extra):
        # log error.
        # prevent 5x error go out at prod
        api_logger.critical("There was a critical error",
                            extra=extra)

        # Ignore GenericException
        data = getattr(response, 'data', {})
        if data.get('status', {}).get('code'):
            return response

        if not settings.DEBUG:
            body = {
                "status": {
                    "message": "",  # TODO: Define message from document
                    "code": "InternalError",
                    "request_id": extra['request_id']
                }
            }
            return JsonResponse(body, status=500)
        return response

    def process_request(self, request):
        # Todo
        # Set or get id request X-Amzn-Trace-Id depend on env
        # now set it uuid default till confirmed!
        self.extra['request_id'] = uuid.uuid4().__str__()

        # set time start
        self.extra['start_time'] = time.time()
        # get abs url and name
        self.extra['uri'] = request.build_absolute_uri()
        self.extra['url_name'] = resolve(request.path).url_name

        # get/set IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        self.extra['ip'] = ip
        request.extra = self.extra

    def process_view(self, request, view_func, view_args, view_kwargs):  # noqa
        # get view and class to the logs
        self.extra['class_name'] = view_func.__name__
        function_name = ""
        if getattr(view_func, 'initkwargs', None):
            function_name = view_func.initkwargs.get('name')

        if getattr(view_func, 'cls', None):
            if request.method.lower() in view_func.cls.http_method_names:
                function_name = request.method.lower()

        if getattr(view_func, 'view_class', None):
            if request.method.lower() in view_func.view_class.http_method_names:
                function_name = request.method.lower()
        self.extra['function_name'] = function_name

    def process_response(self, request, response):
        self.extra['total_time'] = (time.time() - self.extra['start_time'])
        self.extra['status_code'] = response.status_code
        self.extra['method'] = request.method

        # handle error
        if response.status_code >= 500:
            return self.handle_5xx(response, self.extra.copy())
        api_logger.info("", extra=self.extra)

        del request.extra  # Prevent mem leak
        return response
