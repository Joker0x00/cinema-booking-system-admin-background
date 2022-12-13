# Author: wy
# Time: 2022/8/27 10:36
import decimal
import uuid
from hashlib import md5

from django.http import JsonResponse
from django.utils import timezone

from app.utils.Pageination import Pagination
from app.utils.response import Response
from app.utils.loadData import LoadJsonData

from django.views import View
from app.models import Admin, User
from app.utils.UserConfirmService import UserConfirm
from app.utils.TokenService import setToken
from app.utils.TokenService import getUser
from app.utils import rawSQL
from app.utils.InputCheck import CommonPattern


def get_user_info(request):
    user_token = request.GET.get('token')
    role = user_token[len(user_token) - 1]
    user_id = getUser(user_token)
    if not user_id:
        return Response.error('token过期，请重新登陆')
    if role == 'a':
        sql = """
            select `name`, `password`, `role`
            from `admin`
            where `id` = %s
        """
        users = rawSQL.query_all_dict(sql, (user_id,))
        if not len(users):
            return Response.error('用户不存在，请重新登录')
        user = users[0]

        res = {
            'code': 200,
            'data': {
                "roles": user['role'].split(','),
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
            print(user_id)
            return Response.error('用户不存在，请重新登录')
        user = users[0]

        res = {
            'code': 200,
            'data': {
                "roles": ['user'],
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
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    try:
        isAdmin = bool(data.get('isAdmin', False))
    except Exception as e:
        return Response.error('isAdmin类型错误')

    code = data.get('code', '').strip()
    code_id = data.get('code_id', '').strip()

    if not (username != '' and password != '' and isAdmin != '' and code_id != '' and code != ''):
        return Response.error('登录信息不全')

    if not CommonPattern.confirm(CommonPattern.codePattern, code):
        return Response.error('验证码格式错误')

    if len(username) > 50:
        return Response.error('用户名格式错误')

    if len(password) > 50:
        return Response.error('密码格式错误')

    success, message, role = UserConfirm(username, password, isAdmin, code_id, code)

    # 登录失败
    if not success:
        return Response.error(code=404, message=message)
    # 登录成功
    res = {
        "success": success,
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": setToken(message, role),
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
        key = request.GET.get('key', '').strip()

        if len(key) > 50:
            return Response.error('关键字过长')

        sql = 'select `id`, `name`, `create_time`, `role` from admin where `name` like "{}"'.format('%' + key + '%')
        rows = rawSQL.query_all_dict(sql)
        cnt = len(rows)
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取管理员信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})

        name = form['name'].strip()
        if not CommonPattern.confirm(CommonPattern.usernamePattern, name):
            return Response.error('用户名格式错误')

        if not validateName(adminname=name):
            return Response.error('用户名重复')

        password = str(form['password']).strip()
        print(password)
        if not CommonPattern.confirm(CommonPattern.passwordPattern, password):
            return Response.error('密码格式错误')

        raw_roles = list(form['role'])

        if len(raw_roles) <= 0:
            return Response.error('角色列表为空')

        ROLES = ['superAdmin', 'film show manager', 'Comment manager', 'ticket seller']

        roles = ''
        create_time = timezone.now()
        for role in raw_roles:
            if role == 'superAdmin':
                roles = 'superAdmin,'
                break
            if role not in ROLES:
                return Response.error('角色格式错误')
            roles += role + ','
        if roles[len(roles) - 1] == ',':
            roles = roles[:-1]
        sql = 'insert into `admin`' \
              '(`id`, `name`, `password`, `role`, `create_time`) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), name, md5(password.encode("utf-8")).hexdigest(),
                                                       roles, create_time)
        rawSQL.execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        try:
            form = {
                'id': str(raw_form.get('id', '')).strip(),
                'name': str(raw_form.get('name', '')).strip(),
                'password': str(raw_form.get('password', '')).strip(),
                'role': list(raw_form.get('role', '')),
            }
        except Exception as e:
            return Response.error('参数类型错误')

        if not CommonPattern.confirm(CommonPattern.usernamePattern, form['name']):
            return Response.error('用户名格式错误')

        if not validateName(adminname=form['name'], Id=form['id']):
            return Response.error('用户名重复')

        if form['password'] != '' and not CommonPattern.confirm(CommonPattern.passwordPattern, form['password']):
            return Response.error('密码格式错误')

        if len(form['role']) <= 0:
            return Response.error('角色列表为空')

        ROLES = ['superAdmin', 'film show manager', 'Comment manager', 'ticket seller']

        roles = ''
        for role in form['role']:
            if role == 'superAdmin':
                roles = 'superAdmin,'
                break
            print(role)
            if role not in ROLES:
                return Response.error('角色格式错误')
            roles += role + ','
        if roles[len(roles) - 1] == ',':
            roles = roles[:-1]
        form['role'] = roles
        if form['password'] == '':
            sql = 'update `admin` set `name`=%s, `role`=%s where `id`=%s'
            rawSQL.execSql(sql=sql, params=(form['name'], form['role'], form['id']))
        else:
            sql = 'update `admin` set `name`=%s, `password`=%s, `role`=%s where `id`=%s'
            form['password'] = md5(form['password'].encode('utf-8')).hexdigest()
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
        try:
            current_page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            vague = str(request.GET.get('vague', 'false')).strip()
            searchstring = request.GET.get('searchParams', None)
        except Exception:
            return Response.error('参数格式错误')
        vague = True if vague == 'true' else False
        searchParams = [{'key': '', 'value': ''}]

        if searchstring:
            searchParams = eval(searchstring)
        # 处理筛选条件
        condition = {}
        for params in searchParams:
            if params.get('value', ''):
                condition[params['key'] + ('__contains' if vague else '')] = params['value']
        raw_data = User.objects.filter(**condition).values('id', 'name', 'sex', 'phone_number', 'balance')
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
        try:

            form = LoadJsonData(request.body).get_data().get('form', {})
            name = str(form.get('name', '')).strip()
            password = str(form.get('password', '')).strip()
            sex = str(form.get('sex', '')).strip()
            phone_number = str(form.get('form_number', '')).strip()
            balance = decimal.Decimal(form.get('balance', 0.00))

        except Exception:
            return Response.error('参数类型转换错误')

        if not CommonPattern.confirm(CommonPattern.usernamePattern, name):
            return Response.error('用户名格式错误')

        if not CommonPattern.confirm(CommonPattern.passwordPattern, password):
            return Response.error('密码格式错误')

        if phone_number != '' and not CommonPattern.confirm(CommonPattern.numberPattern, phone_number):
            return Response.error('电话号码格式错误')

        if sex != '' and not CommonPattern.confirm(CommonPattern.sexPattern, sex):
            return Response.error('性别格式错误')

        if not CommonPattern.confirm(CommonPattern.moneyPattern, str(balance)):
            return Response.error('金额格式错误')

        Id = uuid.uuid1()

        if not validateName(username=name):
            return Response.error(message='用户名已被占用', code=201)

        sql = 'insert into `user`' \
              '(`id`, `name`, `password`, `sex`, `phone_number`, `balance`) ' \
              'VALUES' \
              '("{}", "{}", MD5("{}"), "{}", "{}", "{}")'.format(Id, name, password, sex, phone_number, balance)
        rawSQL.execSql(sql)
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        try:
            form = {
                'id': str(raw_form.get('id', '')).strip(),
                'name': str(raw_form.get('name', '')).strip(),
                'password': str(raw_form.get('password', '')).strip(),
                'sex': str(raw_form.get('sex', '')).strip(),
                'phone_number': str(raw_form.get('phone_number', '')).strip(),
                'balance': decimal.Decimal(raw_form.get('balance', 0.00))
            }
        except Exception:
            return Response.error('参数类型转换错误')

        if not CommonPattern.confirm(CommonPattern.usernamePattern, form['name']):
            return Response.error('用户名格式错误')

        if not validateName(username=form['name'], Id=form['id']):
            return Response.error('用户名重复')

        if form['password'] != '' and not CommonPattern.codePattern(CommonPattern.passwordPattern, form['password']):
            return Response.error('密码格式错误')

        if form['phone_number'] != '' and not CommonPattern.confirm(CommonPattern.numberPattern, form['phone_number']):
            return Response.error('电话号码格式错误')

        if form['sex'] != '' and not CommonPattern.confirm(CommonPattern.sexPattern, form['sex']):
            return Response.error('性别格式错误')

        if not CommonPattern.confirm(CommonPattern.moneyPattern, str(form['balance'])):
            return Response.error('余额格式错误')

        if form['password'].strip() == '':
            sql = 'update `user` set `name`=%s, `sex`=%s, `phone_number`=%s, `balance`=%s where id=%s'
            params = (form['name'], form['sex'], form['phone_number'], form['balance'], form['id'])
        else:
            sql = 'update `user` set `name`=%s, `password`=MD5(%s), `sex`=%s, `phone_number`=%s, `balance`=%s where id=%s'
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
        params = (user_id,)
        rawSQL.execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()


class UserName(View):
    def get(self, request):
        sql = 'select `id`, `name` from `user`'
        data = rawSQL.query_all_dict(sql)
        return Response.success(data, message='成功获取用户名')


class AdminChangePassView(View):
    def post(self, request):
        form = LoadJsonData(request.body).get_data()
        admin_id = form['id']
        password = form['pass']

        if not CommonPattern.confirm(CommonPattern.passwordPattern, password):
            return Response.error('密码格式错误')

        sql = """
            update `admin`
            set `password` = MD5(%s)
            where id = %s
        """
        rawSQL.execSql(sql, (password, admin_id))
        return Response.success(message='密码修改成功')


class AdminChangeUsernameView(View):
    def post(self, request):
        form = LoadJsonData(request.body).get_data()
        admin_id = form['id']
        username = form['username']

        if not CommonPattern.confirm(CommonPattern.usernamePattern, username):
            return Response.error('用户名格式错误')

        if not validateName(adminname=username, Id=admin_id):
            return Response.error('用户名重复')

        sql = """
            update `admin`
            set `name` = %s
            where id = %s
        """
        rawSQL.execSql(sql, (username, admin_id))
        return Response.success(message='用户名修改成功')


def validateName(username=None, adminname=None, Id=None):
    if username:
        sql = """
            select * from `user`
            where `name` = %s
        """
        data = rawSQL.query_all_dict(sql, (username,))
        exist = len(data)
        print(exist)
        if not exist or exist == 1 and data[0]['id'] == Id:
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
        if not exist or exist == 1 and data[0]['id'] == Id:
            return True
        else:
            return False
    else:
        return False


def editUserInfo(request):
    if request.method == 'POST':
        form = LoadJsonData(request.body).get_data().get('form', {})
        try:
            user_id = str(form.get('id', '')).strip()
            username = str(form.get('username', '')).strip()
            sex = str(form.get('sex', '')).strip()
            phone_number = str(form.get('phone_number', '')).strip()
        except Exception:
            return Response.error('参数类型转换错误')

        if not CommonPattern.confirm(CommonPattern.usernamePattern, username):
            return Response.error('用户名格式错误')

        if phone_number != '' and not CommonPattern.confirm(CommonPattern.numberPattern, phone_number):
            return Response.error('电话号码格式错误')

        if sex != '' and not CommonPattern.confirm(CommonPattern.sexPattern, sex):
            return Response.error('性别格式错误')

        if not validateName(username=username, Id=user_id):
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
        try:
            user_id = str(form['id']).strip()
            password = str(form['pass']).strip()
        except Exception:
            return Response.error('参数类型转换错误')

        if not CommonPattern.confirm(CommonPattern.passwordPattern, password):
            return Response.error('密码格式错误')

        sql = """
                    update `user`
                    set `password` = MD5(%s)
                    where id = %s
                """
        rawSQL.execSql(sql, (password, user_id))
        return Response.success(message='密码修改成功')
    else:
        return Response.error('请求方式错误')
