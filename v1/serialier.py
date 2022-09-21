from rest_framework import serializers


class AddPostSerializer(serializers.Serializer):
  post_type = serializers.CharField(help_text="게시글 종류(Program / Event / News)")
  title = serializers.CharField(help_text="게시글 타이틀")
  start_operating_period = serializers.DateField(help_text="운영 기간 (시작)")
  finish_operating_period = serializers.DateField(help_text="운영 기간 (끝)")
  start_apply_period = serializers.DateField(help_text="?? (시작)")
  finish_apply_period = serializers.DateField(help_text="?? (끝)")
  content = serializers.CharField(help_text="게시글의 글")
  thumbnail = serializers.ImageField(help_text="게시글 썸네일")
  link = serializers.CharField(help_text="게시글 내부에 들어갈 링크")
  disabled = serializers.BooleanField(help_text="게시글 공개 여부")
