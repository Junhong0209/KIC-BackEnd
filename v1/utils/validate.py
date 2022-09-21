from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from .returnStatus import *


def validate(request, key, error_message="", dict_key_error_message="", validation_error_message=""):
  try:
    data = request.data[key]
    return data
  except (KeyError, ValueError):
    return Response(
      status=status.HTTP_400_BAD_REQUEST,
      data=CUSTOM_STATUS_FORM(status=400, message=error_message)
    )
  except MultiValueDictKeyError:
    return Response(
      status=status.HTTP_400_BAD_REQUEST,
      data=CUSTOM_STATUS_FORM(status=400, message=dict_key_error_message)
    )
  except ValidationError:
    return Response(
      status=status.HTTP_400_BAD_REQUEST,
      data=CUSTOM_STATUS_FORM(status=400, message=validation_error_message)
    )