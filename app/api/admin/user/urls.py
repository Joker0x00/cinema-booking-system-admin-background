# Author: wy
# Time: 2022/8/27 10:32
from django.urls import path
from app.views.admin.user.views import login, logout, get_user_info

urlpatterns = [
    path('login/', login),
    path('info/', get_user_info),
    path('logout/', logout)
]