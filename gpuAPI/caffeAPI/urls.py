from django.conf.urls import url,patterns
from caffeAPI import views

urlpatterns = [
   url(r'nearestNeighbour/', views.getNN)
]