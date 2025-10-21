from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('labels/', views.LabelListPublic.as_view(), name='label-list-public'),
    path('labels/<int:pk>/', views.LabelDetailPublic.as_view(), name='label-detail-public'),
    path('albums/', views.AlbumListPublic.as_view(), name='album-list-public'),
    path('albums/<int:pk>/', views.AlbumDetailPublic.as_view(), name='album-detail-public'),
    path('albums/<int:pk>/tracks/', views.AlbumTracksView.as_view(), name='album-tracks'),
    path('artists/', views.ArtistListPublic.as_view(), name='artist-list-public'),
    path('artists/<int:pk>/', views.ArtistDetailPublic.as_view(), name='artist-detail-public'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('adm/labels/', views.LabelListAdmin.as_view(), name='label-list-admin'),
    path('adm/labels/<int:pk>/', views.LabelDetailAdmin.as_view(), name='label-detail-admin'),
    path('adm/albums/', views.AlbumListAdmin.as_view(), name='album-list-admin'),
    path('adm/albums/<int:pk>/', views.AlbumDetailAdmin.as_view(), name='album-detail-admin'),
    path('adm/artists/', views.ArtistListAdmin.as_view(), name='artist-list-admin'),
    path('adm/artists/<int:pk>/', views.ArtistDetailAdmin.as_view(), name='artist-detail-admin'),

    path('albums/<int:pk>/reviews/', views.AlbumReviewsView.as_view(), name='album-reviews'),

    path('', views.index, name='index'),
]
