# Author: wy
# Time: 2022/9/4 20:50
from django.urls import path
from app.views.admin.show.views import ShowView
urlpatterns = [
    path('list/', ShowView.as_view())
]