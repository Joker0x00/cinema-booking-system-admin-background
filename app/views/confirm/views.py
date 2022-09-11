# Author: wy
# Time: 2022/9/10 11:52
import os
import uuid
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django_redis import get_redis_connection
from django.views import View
from app.utils.CodeService import check_code
from app.utils.response import Response


def saveFile(received_file, filename):
    received_file.save(filename)


class ConfirmCode(View):
    def get(self, request):
        img, code = check_code()
        code_id = str(uuid.uuid1())
        conn = get_redis_connection('code')
        conn.set(code_id, code, 60)
        print(code_id, code)
        # stream = BytesIO()
        # img.save(stream, 'png')
        filename = str(uuid.uuid1()) + '.png'
        filepath = os.path.join(settings.MEDIA_ROOT, 'code_img/' + filename)
        saveFile(img, filepath)
        return Response.success(data={
            'url': '/media/show/code_img/' + filename,
            'code_id': code_id
        }, message='获取验证码成功')
