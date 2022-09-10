# Author: wy
# Time: 2022/9/10 11:34

from django.urls import path
from app.views.confirm.views import ConfirmCode
urlpatterns = [
    path('code/', ConfirmCode.as_view())
]