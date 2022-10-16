# Author: wy
# Time: 2022/8/27 20:41
import json
import uuid
from django.db import connection
from django.views import View
from app.models import Movie
from app.models import MovieType
from app import modelViews
from app.utils.Pageination import Pagination
from django.http import JsonResponse

from app.utils.loadData import LoadJsonData
from app.utils.response import Response
from app.utils import rawSQL

def getAllMoive(request):
    sql = 'select * from movie'
    res = rawSQL.query_all_dict(sql)
    data = []
    for m in res:
        m_id = m['id']
        sql = """
            select `score`, `movie`
            from `comment`
            where `movie` = %s
        """
        scores = rawSQL.query_all_dict(sql, (m_id,))
        score = 0
        num = len(scores)
        for s in scores:
            score += s['score']
        if num:
            score /= num
        m['score'] = round(score, 1)
        data.append(m)
    return JsonResponse(Response(code=200, success=True, message='成功获取电影信息', data=data).normal())

class MovieTable(View):
    def get(self, request):
        sql = 'select id, `id` as value, `name` as text, `name` as label from movie'
        res = rawSQL.query_all_dict(sql)
        return JsonResponse(Response(code=200, success=True, message='成功获取电影信息', data=res).normal())

class MovieView(View):
    """获取所有电影分页信息"""

    def get(self, request):
        # 处理参数
        current_page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        vague = request.GET.get('vague', 'false')
        vague = True if vague == 'true' else False
        print(vague)
        searchstring = request.GET.get('searchParams', None)
        searchParams = [{'key': '', 'value': ''}]
        if searchstring:
            searchParams = eval(searchstring)
        # 处理筛选条件
        condition = {}
        for params in searchParams:
            if params.get('value', ''):
                condition[params['key'] + ('__contains' if vague else '')] = params['value']
        print(condition)
        raw_data = modelViews.MovieView.objects.filter(**condition).values()
        raw_data = list(raw_data)
        print(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
            'labels': [['电影编号', 'id'], ['名称', 'name'], ['类型', 'movietypename'], ['主演', 'stars'], ['时长', 'length'],
                       ['简介', 'info'], ['图片', 'image'], ['地区', 'location']]
        }
        # {result: [], page: {total: 100}}
        # Response(code=200, data=data, message='成功获取电影信息').normal()
        return JsonResponse(Response(code=200, data=data, message='成功获取电影信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        print(form['category_id'])
        category = MovieType.objects.filter(id=int(form['category_id'])).first()
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
            'category': raw_form.get('category', ''),
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
