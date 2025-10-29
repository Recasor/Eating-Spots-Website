from django.urls import path
from . import views


urlpatterns = [
    path('', views.canteen, name='canteen'),
    path('menu', views.menu, name='menu'),
    path('reviews', views.reviews, name='reviews'),
    path('settings', views.settings, name='settings'),
    path('exit', views.exit, name='exit'),
    path('scam', views.scam, name='scam'),
    path('profile', views.profile, name='profile'),
    path('canteen_1', views.canteen_1, name='canteen_1'),
    path('canteen_2', views.canteen_2, name='canteen_2'),
    path('canteen_3', views.canteen_3, name='canteen_3'),
    path('canteen_4', views.canteen_4, name='canteen_4'),
    path('canteen_5', views.canteen_5, name='canteen_5'),
]
