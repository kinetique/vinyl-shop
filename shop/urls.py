from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('labels/', views.LabelList.as_view()),
    path('labels/<int:pk>/', views.LabelDetail.as_view()),
    path('albums/', views.AlbumList.as_view()),
    path('albums/<int:pk>/', views.AlbumDetail.as_view()),
    path('albums/<int:pk>/tracks/', views.AlbumTracksView.as_view()),
    path('artists/', views.ArtistList.as_view()),
    path('artists/<int:pk>/', views.ArtistDetail.as_view()),
    path('about/', views.AboutView.as_view()),
    path('', views.index, name='index'),
]
