from django.urls import path
from .views import CoreView

urlpatterns = [
    path('', CoreView.index, name='index'),
    path('login', CoreView.login, name='login'),
    path('logout/', CoreView.logout, name='logout'),
]