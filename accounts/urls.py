from django.urls import path, include
from .views import *

urlpatterns = [
    path('signin/', user_login_view, name='signin'),
    path('signup/', user_register_view, name='signup'),
    path('logout/', user_logout_view, name='logout')
]