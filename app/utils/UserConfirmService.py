# Author: wy
# Time: 2022/9/10 10:46
from django_redis import get_redis_connection
from app.utils import rawSQL


def UserConfirm(username, password, isAdmin, code_id, code):
    conn = get_redis_connection('default')
    c = conn.get(code_id)
    if not c:
        return False, '验证码过期，请重试'
    c = str(c,  encoding="utf-8")
    print(code)
    if c != code.upper():
        return False, '验证码错误'
    # 管理员
    if isAdmin:
        sql = """
            select `id`, `name`, `password`
            from `admin`
            where `name` = %s
        """
        user = rawSQL.query_all_dict(sql, (username, ))
        if not len(user):
            return False, '用户名不存在'
        user = user[0]
        if password != user['password']:
            return False, '密码错误'
        return True, user['id']
    # 普通用户
    else:
        sql = """
                    select `id`, `name`, `password`
                    from `user`
                    where `name` = %s
                """
        user = rawSQL.query_all_dict(sql, (username,))
        if not len(user):
            return False, '用户名不存在'
        user = user[0]
        print(user)
        if password != user['password']:
            return False, '密码错误'
        return True, user['id']
