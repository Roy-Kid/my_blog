from django.urls import path, include
from .views import *

app_name = 'Usermanagement'

urlpatterns = [
    path('edit/<int:id>/', profile_edit, name='edit'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('userdelete/<int:id>/', user_delete, name='delete'),
    ]
