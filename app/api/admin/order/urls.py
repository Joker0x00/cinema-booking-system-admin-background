# Author: wy
# Time: 2022/9/6 15:26


from django.urls import path
from app.views.admin.order.views import OrderView, OrderRefund, recharge

urlpatterns = [
    path('list/', OrderView.as_view()),
    path('refund/<slug:id>/', OrderRefund.as_view()),
    path('recharge/', recharge)
]