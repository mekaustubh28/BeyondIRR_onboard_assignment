import json
import logging
from functools import wraps
from django.http import JsonResponse, HttpResponse
from .models import LogRequests

# Configure logging
logger = logging.getLogger(__name__)

def log_request(record_success):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)

            if response:
                response = response.data

            log = LogRequests(
                url = str(request.build_absolute_uri()),
                method="POST",
                request_payload=response['data'],
                response_payload=response['error'] if 'error' in response else response['message'],
                status_code=int(response['status']),
            )
            if(record_success):
                log.success = (response['status'] < 400)

            log.save()


            return JsonResponse(response)

        return wrapper
    
    return decorator

