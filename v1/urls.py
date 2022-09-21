from django.urls import path
from . import views

urlpatterns = [
  path('post', views.Posting.as_view(), name='post'),
]
