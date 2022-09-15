# Author: wy
# Time: 2022/8/27 16:50
from django.urls import path
from app.views.admin.movie.views import MovieView, MovieTable, getAllMoive

urlpatterns = [
    path('list/', MovieView.as_view()),
    path('all/', MovieTable.as_view()),
    path('movies/', getAllMoive)
]