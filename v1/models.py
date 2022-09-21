from django.db import models


class Post(models.Model):
  id = models.AutoField(verbose_name="id", db_column="id", primary_key=True, null=False, unique=True)
  post_type = models.CharField(verbose_name="post_type", db_column="post_type", max_length=255)
  title = models.CharField(verbose_name="title", db_column="title", max_length=255, default="")
  start_operating_period = models.DateField(verbose_name="start_operating_period", db_column="start_operating_period", default="")
  finish_operating_period = models.DateField(verbose_name="finish_operating_period", db_column="finish_operating_period", default="")
  start_apply_period = models.DateField(verbose_name="start_apply_period", db_column="start_apply_period", default="")
  finish_apply_period = models.DateField(verbose_name="finish_apply_period", db_column="finish_apply_period", default="")
  content = models.TextField(verbose_name="content", db_column="content", default="")
  thumbnail = models.ImageField(verbose_name="thumbnail", db_column="thumbnail", blank=True, null=True, upload_to='uploads')
  link = models.TextField(verbose_name="link", db_column="link", default="")
  disabled = models.BooleanField(verbose_name="post_disabled", db_column="post_disabled", default=False)



