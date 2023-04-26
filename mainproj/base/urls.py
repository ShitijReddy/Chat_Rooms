from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.conf.urls.static import static

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('', views.Home.as_view(), name="home"),
    # path('room', views.room, name="room"),
    path('room/<str:pk>/', views.RoomView.as_view(), name="room"),
    path('room/<str:pk>/search', views.RoomSearch.as_view(), name="room-search"),
    path('profile/<str:pk>/', views.UserProfile.as_view(), name="user-profile"),
    path('create-room/', login_required(views.CreateRoom.as_view(), login_url='login'), name='create-room'),
    path('create-topic/', login_required(views.CreateTopic.as_view(), login_url='login'), name='create-topic'),
    path('create-user/', login_required(views.CreateUser.as_view(), login_url='login'), name='create-user'),
    path('edit-user/', login_required(views.EditUserProfile.as_view(), login_url='login'), name='edit-user'),
    path('update-room/<str:pk>/', login_required(views.UpdateRoom.as_view(), login_url='login'), name='update-room'),
    path('delete-room/<str:pk>/',login_required(views.DeleteRoom.as_view(), login_url='login'), name="delete-room"),
    path('search', views.Search.as_view(), name="search"),
    path('search-user', views.SearchUser.as_view(), name="search-user"),
    path('delete-message/<str:pk>/',login_required(views.DeleteMessage.as_view(), login_url='login'), name="delete-message"),
    path('upvote-message/<str:pk>/',login_required(views.UpvoteMessage.as_view(), login_url='login'), name="upvote-message"),
    path('search-messages/', views.SearchMessages.as_view(), name="search-messages"),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
