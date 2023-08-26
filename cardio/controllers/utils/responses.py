from fastapi import status
from cardio.controllers.utils.models import Error


OK = {status.HTTP_200_OK: {'description': 'Success'}}
NO_CONTENT = {status.HTTP_204_NO_CONTENT: {'description': 'Success'}}
BAD_REQUEST = {status.HTTP_400_BAD_REQUEST: {'description': 'Bad Request', 'model': Error}}
FORBIDDEN = {status.HTTP_403_FORBIDDEN: {'description': 'Forbidden', 'model': Error}}
NOT_FOUND = {status.HTTP_404_NOT_FOUND: {'description': 'Not Found', 'model': Error}}
INTERNAL_SERVER_ERROR = {status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Internal Server Error', 'model': Error}}
