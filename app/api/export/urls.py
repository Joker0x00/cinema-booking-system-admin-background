# Author: wy
# Time: 2022/9/1 21:14

from django.urls import path
from app.views.export.views import TableExportView

urlpatterns = [
    path('table/<slug:table_name>/', TableExportView.as_view())
]