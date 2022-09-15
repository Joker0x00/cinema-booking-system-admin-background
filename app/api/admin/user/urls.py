# Author: wy
# Time: 2022/8/27 10:32
from django.urls import path
from app.views.admin.user.views import login, logout, get_user_info, AdminChangePassView, AdminChangeUsernameView, \
    editUserInfo, userChangePass
from app.views.admin.user.views import AdministratorView, UserView, UserName
urlpatterns = [
    path('login/', login),
    path('info/', get_user_info),
    path('logout/', logout),
    path('admin_list/', AdministratorView.as_view()),
    path('user_list/', UserView.as_view()),
    path('user_name/', UserName.as_view()),
    path('admin_changepass/', AdminChangePassView.as_view()),
    path('admin_changeusername/', AdminChangeUsernameView.as_view()),
    path('editinfo/', editUserInfo),
    path('user_changepass/', userChangePass)
]