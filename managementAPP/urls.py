from django.contrib import admin
from .views import main
from .views import ResidentLoginView, RegisterView
from .views import MessegeList, MessegeDetail, MessegeCreate, MessegeUpdate,  MessegeDelete
from .views import InfoMessegeList, InfoMessegeDetail, InfoMessegeCreate, InfonMessegeUpdate, InfoMessegeDelete
from .views import PollList, PollDetail, PollCreate
from . import views 

from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('login/', ResidentLoginView.as_view(),  name='login'),
    path('logout/', LogoutView.as_view(next_page='login') ,name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('', main.as_view(), name='main'),

    path('messeges/', MessegeList.as_view(), name='messeges'),
    path('messege/<str:pk>/', MessegeDetail.as_view(), name='messege'),
    path('messege-create/', MessegeCreate.as_view(), name='messege-create'),
    path('messege-update/<str:pk>/', MessegeUpdate.as_view(), name='messege-update'),
    path('messege-delete/<str:pk>/', MessegeDelete.as_view(), name='messege-delete'),

    path('infomesseges/', InfoMessegeList.as_view(), name='infomesseges'),
    path('infomessege/<str:pk>/', InfoMessegeDetail.as_view(), name='infomessege'),
    path('infomessege-create/', InfoMessegeCreate.as_view(), name='infomessege-create'),
    path('infomessege-update/<str:pk>/', InfonMessegeUpdate.as_view(), name='infomessege-update'),
    path('infomessege-delete/<str:pk>/', InfoMessegeDelete.as_view(), name='infomessege-delete'),

    path('polls/', PollList.as_view(), name='polls'),
    path('poll/<str:pk>/', PollDetail.as_view(), name='poll'),
    #path('poll-create/', PollCreate.as_view(), name='poll-create'),
    path('poll-create/', views.CreatePoll, name='poll-create'),

    #path('choice/<int:pk>/', hello_world.as_view()),
    #path('choice-create/', hello_world.as_view()),

    #path('vote/<int:pk>/', hello_world.as_view()),
    #path('vote-create/', views.user_register, name='poll-create'),
    path('vote-create/<uuid:pk>/', views.CreateVote, name='vote-create'),    
]