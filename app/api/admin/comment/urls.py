# Author: wy
# Time: 2022/9/7 19:41

from django.urls import path
from app.views.admin.comment.views import CommentView
urlpatterns = [
    path('list/', CommentView.as_view()),
]