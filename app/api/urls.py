# Author: wy
# Time: 2022/8/27 10:43

from django.urls import path, include

bath_path = 'app.api.'

urlpatterns = [
    path('admin/', include(bath_path + 'admin.urls')),
    path('media/', include(bath_path + 'media.urls')),
    path('export/', include(bath_path + 'export.urls')),
    path('confirm/', include(bath_path + 'confirm.urls'))
]