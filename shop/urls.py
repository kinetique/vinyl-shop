from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('albums/', views.AlbumList.as_view()),
    path('albums/<int:pk>/', views.AlbumDetail.as_view()),
    path('', views.index, name='index'),
]
