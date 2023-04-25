from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    path('messages/', views.getAllMessages),
    path('messages/<str:pk>/', views.getMessages),
    path('room-messages/<str:pk>/', views.getRoomMessages),
    path('create-room', views.createRoom),
    path('delete-room/<str:pk>', views.deleteRoom),
    path('update-room/<str:pk>', views.updateRoom),

]
