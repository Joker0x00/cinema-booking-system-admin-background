# Author: wy
# Time: 2022/9/10 10:45
import uuid

from django_redis import get_redis_connection


def setToken(user_id):
    token = str(uuid.uuid1())
    conn = get_redis_connection('token')
    conn.set(token, user_id, 60 * 60 * 24)
    return token

def getUser(token):
    conn = get_redis_connection('token')
    t = conn.get(token)
    if not t:
        return ''
    user_id = str(t, encoding="utf-8")
    return user_id