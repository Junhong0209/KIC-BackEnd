from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serialier import *
from .models import *
from .utils.returnStatus import *
from .utils.validate import validate


@method_decorator(csrf_exempt, name='dispatch')
class Posting(APIView):
  @swagger_auto_schema(
    request_body=AddPostSerializer,
    responses={
      200: "게시글을 성공적으로 작성하였습니다.",
      400: "키가 전달되지 않았습니다. / 잘못된 키가 입력되었습니다. / 날짜 형식이 맞지 않습니다.",
    })
  def post(self, request):
    try:
      post_type = request.data['post_type']
      title = request.data['title']
      content = request.data['content']
      thumbnail = request.data['thumbnail']
      link = request.data['link']
      
      try:
        start_operating_period = request.data['start_operating_period']
        finish_operating_period = request.data['finish_operating_period']
        start_apply_period = request.data['start_apply_period']
        finish_apply_period = request.data['finish_apply_period']
      except ValidationError:
        return Response(
          status=400,
          data=CUSTOM_STATUS_FORM(status=400, message='날짜 형식이 잘못되었습니다.')
        )
      
      posting = Post(
        post_type=post_type,
        title=title,
        start_operating_period=start_operating_period,
        finish_operating_period=finish_operating_period,
        start_apply_period=start_apply_period,
        finish_apply_period=finish_apply_period,
        content=content,
        thumbnail=thumbnail,
        link=link,
      )
      posting.save()
      
      return Response(
        status=status.HTTP_200_OK,
        data=CUSTOM_STATUS_FORM(status=200, message="게시글이 성공적으로 작성되었습니다.")
      )
    except (KeyError, ValueError):
      return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data=CUSTOM_STATUS_FORM(status=400, message="전달되지 않은 키가 존재합니다.")
      )
    except MultiValueDictKeyError:
      return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data=CUSTOM_STATUS_FORM(status=400, message="키가 잘못 입력 되었습니다.")
      )
  
  @swagger_auto_schema(
    responses={
      200: "게시글을 전부 불러왔습니다. / 게시글을 불러왔습니다.",
      400: "게시글을 존재하지 않습니다."
    })
  def get(self, request):
    try:
      post_idx = request.GET['post_idx']
      
      print(post_idx)

      return Response(
        status=200,
        data=CUSTOM_STATUS_FORM(status=200, message='게시글을 불러왔습니다.')
      )
    except MultiValueDictKeyError:
      postings = Post.objects.all()
  
      if not list(postings):
        return Response(
          status=200,
          data=CUSTOM_STATUS_FORM(status=200, message="게시글이 존재하지 않습니다.")
        )
      data = {
        "content": [],
        "number_of_content": 0
      }
      for posting in postings:
        posting_data = {
          "id": posting.id,
          "post_type": posting.post_type,
          "title": posting.title,
          "start_operating_period": posting.start_operating_period,
          "finish_operating_period": posting.finish_operating_period,
          "start_apply_period": posting.start_apply_period,
          "finish_apply_period": posting.finish_apply_period,
          "content": posting.content,
          # 전체 URL을 건네 주는 코드
          "thumbnail": request.build_absolute_uri(posting.thumbnail.url),
          "link": posting.link,
          "disabled": posting.disabled
        }
        data["content"].append(posting_data)
        data["number_of_content"] += 1
      return Response(
        status=status.HTTP_200_OK,
        data=CUSTOM_STATUS_FORM(status=200, message="게시글을 전부 불러왔습니다.", data=data)
      )
    
  @swagger_auto_schema(
    request_body=AddPostSerializer,
    responses={
      200: "게시글이 수정되었습니다."
  })
  def put(self, request):
    post_idx = validate(request=request, key='post_idx', dict_key_error_message='게시글 idx가 존재하지 않습니다.')
    
    try:
      post_data = Post.objects.get(id=post_idx)
    except ObjectDoesNotExist:
      return Response(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=CUSTOM_STATUS_FORM(status=500, message='서버에 게시글이 존재하지 않습니다.')
      )
    
    post_type = validate(request=request, key='post_type', error_message='게시글 종류를 받아오지 못하였습니다.')
    title = validate(request=request, key='title', error_message='게시글 타이틀을 가져오지 못하였습니다.')
    start_operating_period = validate(request=request, key='start_operating_period', error_message='운영 기간을 받아오지 못하였습니다.', validation_error_message='날짜 형식이 알맞지 않습니다.')
    finish_operating_period = validate(request=request, key='finish_operating_period', error_message='운영 기간을 받아오지 못하였습니다.', validation_error_message='날짜 형식이 알맞지 않습니다.')
    start_apply_period = validate(request=request, key='start_apply_period', error_message='게시글 공개 기간을 받아오지 못하였습니다.', validation_error_message='날짜 형식이 알맞지 않습니다.')
    finish_apply_period = validate(request=request, key='finish_apply_period', error_message='게시글 공개 기간을 받아오지 못하였습니다.', validation_error_message='날짜 형식이 알맞지 않습니다.')
    content = validate(request=request, key='content', error_message='게시글 데이터를 받아오지 못하였습니다.')
    thumbnail = validate(request=request, key='thumbnail', error_message='썸네일 사진을 가져오지 못하였습니다.')
    link = validate(request=request, key='link', error_message='링크를 가져오지 못하였습니다.')
    disable = validate(request=request, key='disable', error_message='게시글 공개 여부를 가져오지 못하였습니다.')
    
    post_data.post_type = post_type
    post_data.title = title
    post_data.start_operating_period = start_operating_period
    post_data.finish_operating_period = finish_operating_period
    post_data.start_apply_period = start_apply_period
    post_data.finish_apply_period = finish_apply_period
    post_data.content = content
    post_data.thumbnail = thumbnail
    post_data.link = link
    post_data.disabled = disable
    post_data.save()
    
    return Response(
      status=status.HTTP_200_OK,
      data=CUSTOM_STATUS_FORM(status=200, message='게시글이 성공적으로 수정되었습니다.')
    )
