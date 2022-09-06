# Author: wy
# Time: 2022/9/6 15:30
import uuid

from django.http import JsonResponse
from django.views import View

from app.utils.Pageination import Pagination
from app.models import Order
from app import modelViews
from app.utils.loadData import LoadJsonData
from app.utils.response import Response
from app.utils import rawSQL


class OrderView(View):
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
        # 1
        raw_data = modelViews.OrderDetail.objects.filter(**condition).values()
        raw_data = list(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取订单信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        print(form)
        show_id = form['show_id']
        choose_seat = form['choose_seat']
        user_id = form['user_id']
        sql = 'insert into `order`' \
              '(id, show_id, choose_seat, user_id) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}")'.format(uuid.uuid1(), show_id, choose_seat, user_id)
        print(sql)
        rawSQL.execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'show_id': raw_form.get('movie_id', ''),
            'choose_seat': raw_form.get('choose_seat', ''),
            'user_id': raw_form.get('user_id', '')
        }
        sql = 'update `order` set show_id="%s", choose_seat="%s", user_id="%s" where id="%s"'
        params = (form['show_id'], form['choose_seat'], form['user_id'], form['id'])
        rawSQL.execSql(sql=sql, params=params)
        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        order_id = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Order id:' + order_id)
        if not order_id:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `order` where `id`=%s'
        params = (order_id,)
        data = rawSQL.query_one_dict(sql, params)
        print(data)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `order` where `id`=%s'
        params = (order_id,)
        rawSQL.execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()
