# Author: wy
# Time: 2022/8/28 20:00
import os

from django.views import View
from django.http import JsonResponse
from PIL import Image
import uuid
from app.utils.loadData import LoadJsonData
from django.conf import settings
from app.utils.response import Response

def get_uuid():
    return uuid.uuid1()  # 根据 时间戳生成 uuid , 保证全球唯一


def show(request):
    received_file = request.FILES.get("file")  # upload_name是input按钮的name，必须一样
    try:
        name = str(received_file.name)
    except Exception as e:
        name = '1.jpg'
    types = name[-3:]
    if types != 'jpg' and types != 'png':
        return JsonResponse(Response(code=200, data={
            'filename': '',
            'length': 0,
            'url': ''
        }, success=False, message='上传失败，格式错误'))
    filename = str(get_uuid()) + '.' + types
    filepath = os.path.join(settings.MEDIA_ROOT, 'image/' + filename)
    saveFile(received_file, filepath)

    return JsonResponse({
        'success': 'true',
        'code': 200,
        'filename': received_file.name,
        'length': received_file.size,
        'url': 'http://127.0.0.1:8000/media/show/image/' + filename
    })


# 保存上传的文件
def saveFile(received_file, filename):
    with open(filename, 'wb') as f:
        f.write(received_file.read())


# 读取上传的文件内容，并返回
def readFile(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return content


class ImageView(View):
    def post(self, request):
        return show(request)
