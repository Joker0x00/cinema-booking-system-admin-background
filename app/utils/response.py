# Author: wy
# Time: 2022/8/27 10:22

from django.core import serializers
from django.http.response import JsonResponse


class Response:
    def __init__(self, code, message, success=True, data={}):
        self.data = data
        self.message = message
        self.code = code
        self.success = success

    def model(self):
        self.data = serializers.serialize('json', self.data)
        return {
            'code': self.code,
            'data': self.data,
            'message': self.message,
            'success': self.success,
        }

    def normal(self):
        return {
            'code': self.code,
            'data': self.data,
            'message': self.message,
            'success': self.success
        }

    def jsonResponse(self):
        return JsonResponse({
            'code': self.code,
            'data': self.data,
            'message': self.message,
            'success': self.success,
        })

    @staticmethod
    def error(message="请求失败", code=None):
        if code is None:
            code = 404
        return JsonResponse({
            'code': code,
            'data': '',
            'message': message,
            'success': False,
        })

    @staticmethod
    def success(data=None, message="请求成功", code=None):
        if data is None:
            data = {}
        if code is None:
            code = 200
        return JsonResponse({
            'code': code,
            'data': data,
            'message': message,
            'success': True,
        })
