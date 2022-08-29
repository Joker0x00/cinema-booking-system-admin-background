# Author: wy
# Time: 2022/8/29 20:28
from django.urls import path
from app.views.admin.movie_type.views import MovieTypeView
urlpatterns = [
    path('list/', MovieTypeView.as_view())
]