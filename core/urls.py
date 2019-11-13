from django.urls import path
from .views import CoreView

urlpatterns = [
    path('', CoreView.index, name='index'),
    path('conta', CoreView.conta, name='conta'),
    path('login', CoreView.login, name='login'),
    path('logout/', CoreView.logout, name='logout'),
]