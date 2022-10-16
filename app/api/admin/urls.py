# Author: wy
# Time: 2022/8/27 10:31

from django.urls import path, include

base_path = 'app.api.admin.'

urlpatterns = [
    path('user/', include(base_path + 'user.urls')),
    path('movie/', include(base_path + 'movie.urls')),
    path('movie_type/', include(base_path + 'movie_type.urls')),
    path('room/', include(base_path + 'room.urls')),
    path('show/', include(base_path + 'show.urls')),
    path('order/', include(base_path + 'order.urls')),
    path('comment/', include(base_path + 'comment.urls')),
    path('action/', include(base_path + 'action.urls'))
]