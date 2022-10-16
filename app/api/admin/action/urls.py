# Author: wy
# Time: 2022/10/5 21:03
from django.urls import path

from app.views.admin.action.views import get_log

urlpatterns = [
    path('list/', get_log)
]