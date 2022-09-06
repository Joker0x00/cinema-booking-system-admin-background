# Author: wy
# Time: 2022/8/29 20:30
import uuid

from django.db import connection
from django.views import View
from app.models import MovieType
from app.utils.loadData import LoadJsonData
from django.http.response import JsonResponse

from app.utils.rawSQL import execSql, query_one_dict
from app.utils.response import Response
from app.utils import rawSQL


class MovieTypeView(View):
    def get(self, request):
        key = request.GET.get('key', '')
        print(key)
        sql = 'select id, `id` as value, `name` as text, `name` as label, `name` as name from movie_type where `name` like "{}"'.format('%' + key + '%')
        res = rawSQL.query_all_dict(sql)
        return JsonResponse(Response(code=200, success=True, message='成功获取电影类型', data=res).normal())

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        print(form)
        id = form['id']
        name = form['name']
        sql = 'insert into `movie_type`' \
              '(name) ' \
              'VALUES' \
              ' ("{}")'.format(name)
        print(sql)
        execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', 1),
            'name': raw_form.get('name', '')
        }
        sql = 'update `movie_type` set name=%s where id=%s'
        params = (form['name'], form['id'])
        execSql(sql=sql, params=params)
        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        moiveType_id = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:MovieType id:' + str(moiveType_id))
        if not moiveType_id:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `movie_type` where `id`=%s'
        params = (moiveType_id,)
        data = query_one_dict(sql, params)
        print(data)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `movie_type` where `id`=%s'
        params = (moiveType_id,)
        execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()
