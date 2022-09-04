# Author: wy
# Time: 2022/9/2 21:33

from django.urls import path
from app.views.admin.room.views import RoomView, Room
urlpatterns = [
    path('list/', RoomView.as_view()),
    path('all/', Room.as_view())
]