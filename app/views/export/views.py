# Author: wy
# Time: 2022/9/1 21:18
import json

from django.views import View
from app.utils.response import Response
from app.utils.loadData import LoadJsonData
from app.models import Room
from app.modelViews import MovieView
import csv
from django.http import HttpResponse, StreamingHttpResponse
from app.utils import select


def export_MovieView(request, config):
    for f in config['fields']:
        if f == 'movietypename':
            f = 'movietypeid'
    fields = tuple(config['fields'])
    movies = MovieView.objects.all().values(*fields)
    movies = list(movies)
    print(movies)
    return Response.success(data=movies, message='成功获取文件数据')


def export_Room(request, config):
    fields = tuple(config['fields'])
    objs = Room.objects.all().values(*fields)
    objs = list(objs)
    return Response.success(data=objs, message='成功获取文件数据')


class TableExportView(View):
    def post(self, request, table_name):
        if table_name == '':
            return Response.error('请输入请求表名')
        data = LoadJsonData(request.body).get_data()
        config = data['exportConfig']
        if table_name == 'MovieView':
            return export_MovieView(request, config)
        elif table_name == 'Room':
            return export_Room(request, config)
