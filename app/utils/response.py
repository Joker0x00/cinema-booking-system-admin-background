# Author: wy
# Time: 2022/8/27 10:22

from django.core import serializers


class Response:
    def __init__(self, code, data, message, success=True):
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
