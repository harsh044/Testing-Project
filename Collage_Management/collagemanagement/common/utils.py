from rest_framework import status
from rest_framework.response import Response
from api.messages import messages
import time

def error_response(error):
    return Response(error["error"], error["status"])

def dispatch_response(status_code=None):
    if status_code == 200:
        return Response([], status=status.HTTP_200_OK)
    
    if status_code == 201:
        return Response([], status=status.HTTP_201_CREATED)
    
    if isinstance(status_code, dict) or isinstance(status_code, list):
        data_dict = {
            'status_code': status.HTTP_200_OK,
            'msg': "",
            'response': status_code if isinstance(status_code, list) else [status_code]
        }
        return Response(data_dict, status=status.HTTP_200_OK)
    
    return error_response(messages[status_code])

def generate_password(email):
    millis = int(round(time.time() * 1000))
    password = 'ex@12345'
    new_pass = email[:2]
    new_pass += str(millis)[:-4]
    password = new_pass.upper()
    return password
