from django.urls import path
from .views import *


urlpatterns = [
 path('', index, name='home_view'),
 # path('video/', videocall_view, name='video_view')
 path('video/<str:room>/<str:created>/',video,name='video')
]
