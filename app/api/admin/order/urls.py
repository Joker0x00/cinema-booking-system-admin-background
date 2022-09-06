# Author: wy
# Time: 2022/9/6 15:26


from django.urls import path
from app.views.admin.user.views import login, logout, get_user_info
from app.views.admin.order.views import OrderView
urlpatterns = [
    path('list/', OrderView.as_view())
]