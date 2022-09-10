# Author: wy
# Time: 2022/8/28 15:54


from django.urls import re_path, path
from django.views.static import serve
from django.conf import settings
from app.views.admin.img.views import ImageView
from app.views.confirm.views import ConfirmCode

urlpatterns = [
    re_path(r'show/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('img/', ImageView.as_view()),
    path('code_img/', ConfirmCode.as_view())
]
