from django.conf.urls import url,patterns
from caffeAPI import views

urlpatterns = [
   url(r'nearestNeighbour/', views.getNN),
   url(r'tags/', views.getTags),
   url(r'gpuStatus/', views.getStatus),
]
