# Author: wy
# Time: 2022/8/29 20:30

from django.views import View
from app.models import MovieType
from app.utils.loadData import LoadJsonData
from django.http.response import JsonResponse
from app.utils.response import Response


class MovieTypeView(View):
    def get(self, request):
        res = list(MovieType.objects.values())
        return JsonResponse(Response(code=200, success=True, message='成功获取电影类型', data=res).normal(), safe=False)
