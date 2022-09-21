from drf_yasg import openapi


def CustomResponseSchema(code, detail):
  code_field = openapi.Schema(
    'code',
    description=code,
    type=openapi.TYPE_INTEGER
  )
  
  detail_field = openapi.Schema(
    'detail',
    description=detail,
    type=openapi.TYPE_STRING
  )
  
  error_response = openapi.Schema(
    'response',
    type=openapi.TYPE_OBJECT,
    properties={
      'code': code_field,
      'detail': detail_field
    }
  )
  
  return error_response
