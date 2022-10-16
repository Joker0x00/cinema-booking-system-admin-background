# Author: wy
# Time: 2022/9/2 21:35

import json
import uuid
from django.db import connection
from django.views import View
from app.models import Room
from app import modelViews
from app.utils.Pageination import Pagination
from django.http import JsonResponse

from app.utils.loadData import LoadJsonData
from app.utils.response import Response
from app.utils import rawSQL


class RoomTable(View):
    def get(self, request):
        sql = 'select id, `id` as value, `name` as text, `name` as label from room'
        res = rawSQL.query_all_dict(sql)
        return JsonResponse(Response(code=200, success=True, message='成功获取放映厅', data=res).normal())


class RoomView(View):
    """获取所有放映厅分页信息"""

    def get(self, request):
        # 处理参数
        current_page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        vague = request.GET.get('vague', 'false')
        vague = True if vague == 'true' else False
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
        raw_data = Room.objects.filter(**condition).values()
        raw_data = list(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取放映厅信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        print(form)
        obj = Room(
            id=uuid.uuid1(),
            name=form['name'],
            size=form['size'],
            seat_layout=form['seat_layout'],
            row=form['row'],
            column=form['column'],
            offset=form['offset'],
            screen_width=form['screen_width']
        )
        obj.save()
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'name': raw_form.get('name', ''),
            'row': raw_form.get('row', ''),
            'column': raw_form.get('column', ''),
            'size': raw_form.get('size', ''),
            'screen_width': raw_form.get('screen_width', ''),
            'offset': raw_form.get('offset', ''),
            'seat_layout': raw_form.get('seat_layout', '')
        }
        # 数据验证和处理
        obj = Room.objects.filter(id=form['id']).first()
        obj.name = form['name']
        obj.row = form['row']
        obj.column = form['column']
        obj.seat_layout = form['seat_layout']
        obj.size = form['size']
        obj.screen_width = form['screen_width']
        obj.offset = form['offset']

        obj.save()

        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        roomId = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Room id:' + roomId)
        if not roomId:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        obj = Room.objects.filter(id=roomId).first()
        if not obj:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        obj.delete()
        return Response(code=200, success=True, message='删除成功').jsonResponse()


class RoomDetail(View):
    def get(self, request):
        movie_id = request.GET.get('movie_id', '')
        if not movie_id:
            return Response.error('需要电影id')
        sql = """
            SELECT DISTINCT
                room.id AS id, 
                room.`name` AS `name`
            FROM
                `show`
                INNER JOIN
                    room
                ON 
                    `show`.room = room.id
                INNER JOIN
                    movie
                ON 
                    `show`.movie = movie.id
            WHERE `show`.`movie` = %s and `show`.`status` = '即将上映'
        """
        data = rawSQL.query_all_dict(sql, params=(movie_id,))
        print(data)
        return Response.success(data=data, message='成功获取放映厅数据')