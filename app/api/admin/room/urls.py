# Author: wy
# Time: 2022/9/2 21:33

from django.urls import path
from app.views.admin.room.views import RoomView, RoomTable, RoomDetail
urlpatterns = [
    path('list/', RoomView.as_view()),
    path('all/', RoomTable.as_view()),
    path('detail/', RoomDetail.as_view())
]