# Author: wy
# Time: 2022/9/6 15:30
import decimal
import uuid

from django.http import JsonResponse
from django.utils import timezone
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
        show_id = form['show_id']
        choose_seat = form['choose_seat']
        user_id = form['user_id']
        num = form['num']
        total_price = float(form['total_price'])
        status = form['status']
        layout = form['layout']
        # 余额是否够
        sql = """
            select `balance`
            from `user`
            where `id` = %s
        """
        user_balance = (rawSQL.query_one_dict(sql, (user_id,)))['balance']
        if user_balance < total_price:
            return Response.error('余额不足')
        # 新增订单
        sql = 'insert into `order`' \
              '(id, show_id, choose_seat, user_id, create_time, num, total_price, status) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}" ,"{}", "{}", "{}", "{}")'.format(uuid.uuid1(), show_id, choose_seat, user_id,
                                                                         timezone.now(), num, total_price, status)
        rawSQL.execSql(sql)
        # 更新show的座位布局
        sql = """
            update `show`
            set `seat_layout` = %s
            where `id` = %s
        """
        rawSQL.execSql(sql, (layout, show_id))
        # 用户余额划款
        user_balance -= decimal.Decimal(total_price)
        print(user_balance)
        sql = """
            update `user`
            set `balance` = %s
            where `id` = %s
        """
        rawSQL.execSql(sql, (user_balance, user_id))
        return Response.success(message='新增成功')

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


class OrderRefund(View):
    def post(self, request, id):
        if not id:
            return Response.error(message='需提供id')
        sql = """
            select `user`.id as user_id, `user`.balance as user_balance, `order`.total_price as total_price
            from `user`
                inner join
                `order`
                on `user`.id = `order`.user_id
            where `order`.id = %s
        """
        info = rawSQL.query_one_dict(sql, (id,))
        user_id = info['user_id']
        user_balance = info['user_balance']
        user_balance += info['total_price']
        sql = """
            update `user`
            set `balance` = %s
            where `id` = %s
        """
        rawSQL.execSql(sql, (user_balance, user_id))
        sql = """
            update `order`
            set `status` = '已退票'
            where `id` = %s
        """
        rawSQL.execSql(sql, params=(id,))
        return Response.success(message='退票成功')


def recharge(request):
    if request.method == 'POST':
        form = LoadJsonData(request.body).get_data()
        user_id = form.get('id', '')
        plus = form.get('plus', '')
        try:
            plus = float(plus)
        except Exception as e:
            plus = 0.0
            return Response.error('数据格式错误')
        sql = """
            update `user`
            set `balance` = %s + `balance`
            where `id` = %s
        """
        rawSQL.execSql(sql, (plus, user_id))
        return Response.success('充值成功')
    else:
        return Response.error('请求方式错误')
