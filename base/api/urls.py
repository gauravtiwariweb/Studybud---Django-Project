from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),    # we will directly add it in urls.py of our main project/
    path('rooms/',views.getRooms),
    path('room/<str:pk>/',views.getRoom),
]
