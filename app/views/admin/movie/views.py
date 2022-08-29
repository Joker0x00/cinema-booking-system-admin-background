# Author: wy
# Time: 2022/8/27 20:41
import uuid

from django.views import View
from app.models import Movie
from app.models import MovieType
from app.utils.Pageination import Pagination
from django.http import JsonResponse

from app.utils.loadData import LoadJsonData
from app.utils.response import Response


class MovieView(View):
    """获取所有电影分页信息"""

    def get(self, request):
        current_page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        raw_data = Movie.objects.values()
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start : end]
        data = {
            'count': cnt,
            'rows': rows,
            'labels': [['电影编号', 'id'], ['名称', 'name'], ['类型', 'category_id'], ['主演', 'stars'], ['时长', 'length'], ['简介', 'info'], ['图片', 'image'], ['地区', 'location']]
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取电影信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        category = MovieType.objects.filter(id=form['category_id']).first()
        print(form['image'][5:])
        url = form['image'][5:]
        obj = Movie(id=uuid.uuid1(), name=form['name'], category=category, stars=form['stars'], length=form['length'], info=form['info'], image=url, location=form['location'])
        print(obj)
        obj.save()
        return JsonResponse(Response(code=200, success=True, message='新增成功').normal())