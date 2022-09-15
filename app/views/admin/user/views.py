# Author: wy
# Time: 2022/8/27 10:36
import uuid

from django.http import JsonResponse
from django.utils import timezone
from django_redis import get_redis_connection
from django.views.decorators.csrf import csrf_exempt

from app.utils.Pageination import Pagination
from app.utils.response import Response
from app.utils.loadData import LoadJsonData
from app.utils import rawSQL
from app.utils.CodeService import check_code
from django.views import View
from app.models import Admin, User
from app.utils.UserConfirmService import UserConfirm
from app.utils.TokenService import setToken
from app.utils.TokenService import getUser
from app.utils import rawSQL
def get_user_info(request):
    user_token = request.GET.get('token')
    role = request.GET.get('role')
    user_id = getUser(user_token)
    print(role)
    if not user_id:
        return Response.error('登录过期，请重新登陆')
    if role == 'admin':
        sql = """
            select `name`, `password`, `role`
            from `admin`
            where `id` = %s
        """
        users = rawSQL.query_all_dict(sql, (user_id, ))
        if not len(users):
            return Response.error('登录过期，请重新登录')
        user = users[0]

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
                "role": user['role'],
                "id": user_id,
                "name": user['name'],
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
            },
            'message': '成功登录',
            'success': True
        }
        return JsonResponse(res)
    else:
        sql = """
                    select `name`, `password`, `sex`, `phone_number`, `balance`
                    from `user`
                    where `id` = %s
                """
        users = rawSQL.query_all_dict(sql, (user_id,))
        if not len(users):
            return Response.error('登录过期，请重新登录')
        user = users[0]

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
                "role": 'user',
                "id": user_id,
                "name": user['name'],
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                "sex": user['sex'],
                "phone_number": user['phone_number'],
                "balance": user['balance']
            },
            'message': '成功登录',
            'success': True
        }
        return JsonResponse(res)

# 登录
def login(request):
    data = LoadJsonData(request.body).get_data()
    username = data.get('username', '')
    password = data.get('password', '')
    isAdmin = data.get('isAdmin', '')
    code = data.get('code', '')
    code_id = data.get('code_id', '')
    print(data)
    if not (username != '' and password != '' and isAdmin != '' and code_id != '' and code != ''):
        return Response.error('登录信息不全')
    success, message, role = UserConfirm(username, password, isAdmin, code_id, code)
    # 登录失败
    if not success:
        return Response.error(message)
    # 登录成功
    res = {
        "success": success,
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": setToken(message),
            "role": role
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
        balance = form.get('balance', 0)
        sql = 'insert into `user`' \
              '(`id`, `name`, `password`, `sex`, `phone_number`, `balance`) ' \
              'VALUES' \
              '("{}", "{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), name, password, sex, birthday, phone_number, balance)
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
            'balance': float(raw_form.get('balance', 0))
        }
        sql = 'update `user` set `name`=%s, `password`=%s, `sex`=%s, `phone_number`=%s, `balance`=%s where id=%s'
        params = (form['name'], form['password'], form['sex'], form['phone_number'], form['balance'], form['id'])
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


class AdminChangePassView(View):
    def post(self, request):
        form = LoadJsonData(request.body).get_data()
        admin_id = form['id']
        password = form['pass']
        sql = """
            update `admin`
            set `password` = %s
            where id = %s
        """
        rawSQL.execSql(sql, (password, admin_id))
        return Response.success(message='密码修改成功')

class AdminChangeUsernameView(View):
    def post(self, request):
        form = LoadJsonData(request.body).get_data()
        admin_id = form['id']
        username = form['username']
        sql = """
            update `admin`
            set `name` = %s
            where id = %s
        """
        rawSQL.execSql(sql, (username, admin_id))
        return Response.success(message='用户名修改成功')

def validateName(username=None, adminname=None):
    if username:
        sql = """
            select * from `user`
            where `name` = %s
        """
        data = rawSQL.query_all_dict(sql, (username,))
        exist = len(data)
        if not exist or exist == 1 and data[0]['name'] == username:
            return True
        else:
            return False
    elif adminname:
        sql = """
            select * from `admin`
            where `name` = %s
        """
        data = rawSQL.query_all_dict(sql, (adminname,))
        exist = len(data)
        if not exist or exist == 1 and data[0]['name'] == adminname:
            return True
        else:
            return False
    else:
        return False


def editUserInfo(request):
    if request.method == 'POST':
        form = LoadJsonData(request.body).get_data().get('form', {})
        user_id = form.get('id', '')
        username = form.get('username', '')
        sex = form.get('sex', '')
        phone_number = form.get('phone_number', '')
        if not validateName(username=username):
            return Response.error(201, '用户名已被占用')
        sql = """
            update `user`
            set `name` = %s, `sex` = %s, `phone_number` = %s
            where `id` = %s
        """
        rawSQL.execSql(sql, (username, sex, phone_number, user_id))
        return Response.success('修改成功')

    else:
        Response.error('请求方式错误')

def userChangePass(request):
    if request.method == 'POST':
        form = LoadJsonData(request.body).get_data()
        user_id = form['id']
        password = form['pass']
        sql = """
                    update `user`
                    set `password` = %s
                    where id = %s
                """
        rawSQL.execSql(sql, (password, user_id))
        return Response.success(message='密码修改成功')
    else:
        return Response.error('请求方式错误')