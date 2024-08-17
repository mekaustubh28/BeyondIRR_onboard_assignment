import json
import logging
from functools import wraps
from django.http import JsonResponse, HttpResponse
from .models import LogRequests

# Configure logging
logger = logging.getLogger(__name__)

def log_request(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)

        if response:
            response = response.data

        log = LogRequests(
            url = str(request.build_absolute_uri()),
            method="POST",
            request_payload=response['data'],
            response_payload=response['error'],
            status_code=int(response['status']),
            success=(response['status'] < 400)
        )

        print(log)
        log.save()


        return JsonResponse(response)

    return wrapper

