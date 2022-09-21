def CUSTOM_STATUS_FORM(status=200, message='message', data={}):
  STATUS_FORM = {
    'status': status,
    'detail': message,
    'data': data
  }
  return STATUS_FORM
