# Author: wy
# Time: 2022/9/4 20:52
import datetime

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
from app.utils import rawSQL, Validate
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
        raw_data = modelViews.ShowView.objects.filter(**condition).values().order_by('-start_time')
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
        movie_id = form['movie_id']
        room_id = form['room_id']
        sql = """
            select `length`
            from `movie`
            where `movie`.`id` = %s
        """
        movie_length = query_one_dict(sql, (movie_id,))['length']
        movie_length = int(movie_length)
        sql = """
            select seat_layout
            from `room`
            where `id` = %s
        """
        seat_layout = (rawSQL.query_one_dict(sql, params=(room_id,)))['seat_layout']
        print(form['start_time'])
        dateTime = form['start_time'].split('T')
        date = dateTime[0]
        time = dateTime[1].split('.')[0]
        t = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M:%S")
        t_new = t + datetime.timedelta(hours=8)

        status = Validate.validateShowTime(room_id, t_new, t_new + datetime.timedelta(minutes=movie_length))
        if not status:
            return Response.error('时间冲突')
        sql = 'insert into `show`' \
              '(id, movie, room, start_time, price, seat_layout, status) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), movie_id, room_id, t_new,
                                                                   form['price'],
                                                                   seat_layout, form['status'])
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
            'status': raw_form.get('status', '')
        }
        dateTime = form['start_time'].split('T')
        date = dateTime[0]
        time = dateTime[1].split('.')[0]
        movie_id = form['movie_id']
        room_id = form['room_id']
        sql = """
            select `length`
            from `movie`
            where `movie`.`id` = %s
        """
        movie_length = query_one_dict(sql, (movie_id,))['length']
        movie_length = int(movie_length)
        t = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M:%S")
        if '.' in dateTime[1]:
            t += datetime.timedelta(hours=8)

        status = Validate.validateShowTime(room_id, t, t + datetime.timedelta(minutes=movie_length), show_id=form['id'])
        if not status:
            return Response.error('时间冲突')
        sql = 'update `show` set `movie` = %s, `room` = %s, start_time = %s, price = %s, status = %s where id = %s'
        params = (form['movie_id'], form['room_id'], t, form['price'], form['status'], form['id'])
        execSql(sql=sql, params=params)
        if not updateOrderStatus(form['id'], form['status']):
            return Response.error(message='修改订单状态失败')
        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        showId = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Show id:' + showId)
        if not showId:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `show` where `id`=%s'
        params = (showId,)
        data = query_one_dict(sql, params)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `show` where `id`=%s'
        params = (showId,)
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
            layout = (rawSQL.query_one_dict(sql, params=(show_id,)))
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
        data = rawSQL.query_all_dict(sql, params=(movie_id, room_id))
        return Response.success(data, message='成功获取放映数据')


def getAllShow(request):
    movie_id = request.GET.get('movie_id', '')
    if not movie_id:
        return Response.error('缺少参数')
    sql = """
        select `show`.`id` AS `id`,`movie`.`name` AS `movieName`,`movie`.`length` AS `length`,
        `room`.`name` AS `roomName`,`room`.`size` AS `size`,`room`.`column` AS `column`,`room`.`row` AS `row`,
        `show`.`start_time` AS `start_time`,`show`.`price` AS `price`,`movie`.`id` AS `movie_id`,`room`.`id` AS `room_id`,
        `show`.`seat_layout` AS `seat_layout` from ((`show` join `room` on((`show`.`room` = `room`.`id`))) join `movie` 
        on((`show`.`movie` = `movie`.`id`)))
        where `movie`.`id` = %s
        order by `show`.`start_time`
    """
    data = rawSQL.query_all_dict(sql, (movie_id,))
    return Response.success(data)


def getSeatInfo(request):
    show_id = request.GET.get('show_id', '')
    if not show_id:
        return Response.error('缺少参数')
    sql = """
        select `id`, `price`, `seat_layout`
    """


def updateOrderStatus(Id, status):
    sql = ''
    print(status)
    if status == '即将上映':
        sql = """
            update `order`
            set `status` = '未完成'
            where `show_id` = %s and `status` = '已完成'
        """
    else:
        sql = """
            update `order`
            set `status` = '已完成'
            where `show_id` = %s and `status` = '未完成'
        """
    rawSQL.execSql(sql, (Id, ))
    return True
