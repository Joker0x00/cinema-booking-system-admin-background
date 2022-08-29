# Author: wy
# Time: 2022/8/27 10:31

from django.urls import path, include

base_path = 'app.api.admin.'

urlpatterns = [
    path('user/', include(base_path + 'user.urls')),
    path('movie/', include(base_path + 'movie.urls')),
]