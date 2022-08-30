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
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
            'labels': [['电影编号', 'id'], ['名称', 'name'], ['类型', 'category_id'], ['主演', 'stars'], ['时长', 'length'],
                       ['简介', 'info'], ['图片', 'image'], ['地区', 'location']]
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取电影信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        category = MovieType.objects.filter(id=form['category_id']).first()
        print(form['image'][5:])
        url = form['image'][5:]
        print(url)
        obj = Movie(id=uuid.uuid1(), name=form['name'], category=category, stars=form['stars'], length=form['length'],
                    info=form['info'], image=url, location=form['location'])
        obj.save()
        return JsonResponse(Response(code=200, success=True, message='新增成功').normal())

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'name': raw_form.get('name', ''),
            'category': raw_form.get('category_id', ''),
            'stars': raw_form.get('stars', ''),
            'length': raw_form.get('length', ''),
            'info': raw_form.get('info', ''),
            'image': raw_form.get('image', ''),
            'location': raw_form.get('location', '')
        }
        # 数据验证和处理

        form['category'] = MovieType.objects.filter(id=form['category']).first()
        obj = Movie.objects.filter(id=form['id']).first()
        obj.name = form['name']
        obj.category = form['category']
        obj.stars = form['stars']
        obj.length = form['length']
        obj.info = form['info']
        obj.image = form['image']
        obj.location = form['location']

        obj.save()

        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        movieId = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Movie id:' + movieId)
        if not movieId:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        obj = Movie.objects.filter(id=movieId).first()
        if not obj:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        obj.delete()
        return Response(code=200, success=True, message='删除成功').jsonResponse()