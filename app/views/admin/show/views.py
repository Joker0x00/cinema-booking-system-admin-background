# Author: wy
# Time: 2022/9/4 20:52
from django.views import View
from app import modelViews
from app.models import Show, Movie, Room
import json
import uuid
from django.db import connection
from app.utils.Pageination import Pagination
from django.http import JsonResponse
from app.utils.loadData import LoadJsonData
from app.utils.response import Response
from app.utils import rawSQL
from app.utils.rawSQL import execSql, query_one_dict

class ShowView(View):
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
        raw_data = modelViews.ShowView.objects.filter(**condition).values()
        raw_data = list(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取放映信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        print(form)
        movie_id = form['movie_id']
        room_id = form['room_id']
        sql = """
            select seat_layout
            from `room`
            where `id` = %s
        """
        seat_layout = (rawSQL.query_one_dict(sql, params=(room_id, )))['seat_layout']
        dateTime = form['start_time'].split('T')
        date = dateTime[0]
        time = dateTime[1].split('.')[0]
        print(date + ' ' + time)
        sql = 'insert into `show`' \
              '(id, movie, room, start_time, price, seat_layout) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), movie_id, room_id, date + ' ' + time, form['price'], seat_layout)
        print(sql)
        execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'movie_id': raw_form.get('movie_id', ''),
            'room_id': raw_form.get('room_id', ''),
            'start_time': raw_form.get('start_time', ''),
            'price': raw_form.get('price', ''),
        }
        dateTime = form['start_time'].split('T')
        date = dateTime[0]
        time = dateTime[1].split('Z')[0]
        sql = 'update `show` set movie="%s", room="%s", start_time="%s", price="%s" where id="%s"'
        params = (form['movie_id'], form['room_id'], date + ' ' + time, form['price'], form['id'])
        execSql(sql=sql, params=(form['movie_id'], form['room_id'], date + ' ' + time, form['price'], form['id']))
        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        showId = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Show id:' + showId)
        print(showId)
        if not showId:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `show` where `id`=%s'
        params = (showId,)
        data = query_one_dict(sql, params)
        print(data)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `show` where `id`=%s'
        params = (showId, )
        execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()


class ShowDetail(View):
    def get(self, request):
        movie_id = request.GET.get('movie_id', '')
        room_id = request.GET.get('room_id', '')
        show_id = request.GET.get('show_id', '')
        if show_id:
            sql = """
                SELECT
                    `show`.seat_layout AS seat_layout, 
                    room.size AS size, 
                    room.`column` AS `column`, 
                    room.`row` AS `row`, 
                    room.`offset` AS `offset`, 
                    room.screen_width AS screen_width
                FROM
                    `show`
                    INNER JOIN
                    room
                    ON 
                        `show`.room = room.id
                WHERE `show`.id = %s
            """
            layout = (rawSQL.query_one_dict(sql, params=(show_id, )))
            return Response.success(layout, '成功获取放映厅信息和座位数据')
        if not movie_id or not room_id:
            return Response.error('需要电影id或放映厅id')
        sql = """
            SELECT
                `show`.id AS show_id, 
                `show`.start_time AS start_time, 
                `show`.price AS price
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
            WHERE `show`.`movie` = %s AND `show`.`room` = %s
        """
        print(movie_id)
        print(room_id)
        data = rawSQL.query_all_dict(sql, params=(movie_id, room_id))
        print(data)
        return Response.success(data, message='成功获取放映数据')