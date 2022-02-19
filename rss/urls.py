from django.urls import path

from . import views

urlpatterns = [
    path('rss', views.IndexView.as_view(), name='index'),
    path('rss/<int:feed_id>/', views.detail, name='detail'),
    path('new', views.detail, name='create')
]