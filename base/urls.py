from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    
    
    # path('room/',views.room,name='room'),
    path('room/<str:pk>/',views.room,name='room'),  # here pk is not primary key , it is the name through which we want to access the value , it can be id or anything but it should be a primary key because we will be needing unique and not-null value
    
    # it can be other thing and of other types also
    # path('room/<slug>/',views.room,name='room'), # here slug is a field which we can create while creating a model and can pass a unique type of url
    # path('room/<int:id>/',views.room,name='room'),
    
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path("delete-room/<str:pk>/",views.deleteRoom, name="delete-room"),
    path("login/",views.loginView,name="login"),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name="register"),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    path('edit-message/<str:pk>/',views.editMessage,name='edit-message'),
    path("profile/<str:pk>/", views.userProfile, name="profile"),
    path('update-user/',views.updateUser,name='update-user'),
    path('browse-topics/',views.topicsPage,name='topics'),
    path('browse-activities/',views.activitiesPage,name='activities'),
    
]

