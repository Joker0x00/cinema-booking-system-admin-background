# Author: wy
# Time: 2022/8/27 10:36
import uuid

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from app.utils.Pageination import Pagination
from app.utils.response import Response
from app.utils.loadData import LoadJsonData
from app.utils import rawSQL
from django.views import View
from app.models import Admin, User

def get_user_info(request):
    # print(request.GET.get('token'))
    res = {
        'code': 200,
        'data': {
            "routes": [
                "A",
                "User",
                "Category",
                "Discount",
                "ActivityEdit",
                "CouponRule",
                "Product",
                "Activity",
                "CouponAdd",
                "Trademark",
                "Attr",
                "ActivityAdd",
                "Test3",
                "Test2",
                "CouponEdit",
                "OrderShow",
                "Test",
                "Permission",
                "Spu",
                "UserList",
                "ClientUser",
                "consumer",
                "Order",
                "Coupon",
                "test123321",
                "Banner",
                "Acl",
                "ActivityRule",
                "Role",
                "RoleAuth",
                "Test1",
                "Refund",
                "consumerlist",
                "OrderList",
                "Sku",
                "TradeMark"
            ],
            "buttons": [
                "cuser.detail",
                "cuser.update",
                "cuser.delete",
                "btn.User.add",
                "btn.User.remove",
                "btn.User.update",
                "btn.User.assgin",
                "btn.Role.assgin",
                "btn.Role.add",
                "btn.Role.update",
                "btn.Role.remove",
                "btn.Permission.add",
                "btn.Permission.update",
                "btn.Permission.remove",
                "btn.Activity.add",
                "btn.Activity.update",
                "btn.Activity.rule",
                "btn.Coupon.add",
                "btn.Coupon.update",
                "btn.Coupon.rule",
                "btn.OrderList.detail",
                "btn.OrderList.Refund",
                "btn.UserList.lock",
                "btn.Category.add",
                "btn.Category.update",
                "btn.Category.remove",
                "btn.Trademark.add",
                "btn.Trademark.update",
                "btn.Trademark.remove",
                "btn.Attr.add",
                "btn.Attr.update",
                "btn.Attr.remove",
                "btn.Spu.add",
                "btn.Spu.addsku",
                "btn.Spu.update",
                "btn.Spu.skus",
                "btn.Spu.delete",
                "btn.Sku.updown",
                "btn.Sku.update",
                "btn.Sku.detail",
                "btn.Sku.remove",
                "btn.Role.a",
                "btn.add1",
                "btn.add2",
                "btn.Add3",
                "btn.edit"
            ],
            "roles": [
                "普通员工"
            ],
            "name": "admin",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
        },
        'message': '成功登录',
        'success': True
    }
    return JsonResponse(res)

# 登录
def login(request):
    data = LoadJsonData(request.body).get_data()
    res = {
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "token": "eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJSSkzJzcxT0lFKrShQsjI0MzM0NTI2NTaqBQCV9puSIAAAAA.awM_i4jsrGgU7pJScZ1LKGy2Es82oMa23WezBKAKeDjO27-yccTC_nTPkQmvQvB2_qrTK44GZEXRA9qb1mpD3Q"
        }
    }
    return JsonResponse(res)

# 登出
def logout(request):
    res = {
        "success": True,
        "code": 200,
        "message": "成功",
        "data": {}
    }
    return JsonResponse(res)


class AdministratorView(View):
    def get(self, request):
        key = request.GET.get('key', '')
        sql = 'select * from admin where `name` like "{}"'.format('%' + key + '%')
        rows = rawSQL.query_all_dict(sql)
        cnt = len(rows)
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取管理员信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        name = form['name']
        password = form['password']
        raw_roles = form['role']
        roles = ''
        create_time = timezone.now()
        for role in raw_roles:
            if role == 'superAdmin':
                roles = 'superAdmin,'
                break
            roles += role + ','
        if roles[len(roles) - 1] == ',':
            roles = roles[:-1]
        sql = 'insert into `admin`' \
              '(`id`, `name`, `password`, `role`, `create_time`) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), name, password, roles, create_time)
        rawSQL.execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'name': raw_form.get('name', ''),
            'password': raw_form.get('password', ''),
            'role': raw_form.get('role', ''),
        }
        roles = ''
        for role in form['role']:
            if role == 'superAdmin':
                roles = 'superAdmin,'
                break
            roles += role + ','
        if roles[len(roles) - 1] == ',':
            roles = roles[:-1]
        form['role'] = roles
        sql = 'update `admin` set `name`=%s, `password`=%s, `role`=%s where `id`=%s'
        rawSQL.execSql(sql=sql, params=(form['name'], form['password'], form['role'], form['id']))
        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        adminId = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Admin id:' + adminId)
        if not adminId:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `admin` where `id`=%s'
        params = (adminId,)
        data = rawSQL.query_one_dict(sql, params)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `admin` where `id`=%s'
        params = (adminId,)
        rawSQL.execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()


class UserView(View):
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
        raw_data = User.objects.filter(**condition).values()
        raw_data = list(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取用户信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        name = form.get('name', '')
        password = form.get('password', '')
        sex = form.get('sex', '')
        birthday = form.get('birthday', '')
        phone_number = form.get('form_number', '')
        sql = 'insert into `user`' \
              '(`id`, `name`, `password`, `sex`, `phone_number`) ' \
              'VALUES' \
              '("{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), name, password, sex, birthday, phone_number)
        rawSQL.execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'name': raw_form.get('name', ''),
            'password': raw_form.get('password', ''),
            'sex': raw_form.get('sex', ''),
            'phone_number': raw_form.get('phone_number', ''),
        }
        sql = 'update `user` set `name`=%s, `password`=%s, `sex`=%s, `phone_number`=%s where id=%s'
        params = (form['name'], form['password'], form['sex'], form['phone_number'], form['id'])
        rawSQL.execSql(sql=sql, params=params)
        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        user_id = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:User id:' + user_id)
        if not user_id:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `user` where `id`=%s'
        params = (user_id,)
        data = rawSQL.query_one_dict(sql, params)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `user` where `id`=%s'
        params = (user_id, )
        rawSQL.execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()


class UserName(View):
    def get(self, request):
        sql = 'select `id`, `name` from `user`'
        data = rawSQL.query_all_dict(sql)
        print(data)
        return Response.success(data, message='成功获取用户名')