# Author: wy
# Time: 2022/9/1 21:18
import json

from django.views import View
from app.utils.response import Response
from app.utils.loadData import LoadJsonData
from app.models import Room, MovieType, Admin, User
from app.modelViews import MovieView, ShowView, OrderDetail
import csv
from django.http import HttpResponse, StreamingHttpResponse
from app.utils import rawSQL


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


def export_ShowView(request, config):
    # for f in config['fields']:
    #     if f == 'movie_id':
    #         f = 'movie'
    #     if f == 'room_id':
    #         f = 'room'
    fields = tuple(config['fields'])
    objs = ShowView.objects.all().values(*fields)
    objs = list(objs)
    return Response.success(data=objs, message='成功获取文件数据')

def export_MovieType(request, config):
    fields = tuple(config['fields'])
    objs = MovieType.objects.all().values(*fields)
    objs = list(objs)
    return Response.success(data=objs, message='成功获取文件数据')

def export_Admin(request, config):
    fields = tuple(config['fields'])
    objs = Admin.objects.all().values(*fields)
    objs = list(objs)
    return Response.success(data=objs, message='成功获取文件数据')

def export_User(request, config):
    fields = tuple(config['fields'])
    objs = User.objects.all().values(*fields)
    objs = list(objs)
    return Response.success(data=objs, message='成功获取文件数据')

def export_Order(request, config):
    fields = tuple(config['fields'])
    objs = OrderDetail.objects.all().values(*fields)
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
        elif table_name == 'ShowView':
            return export_ShowView(request, config)
        elif table_name == 'MovieType':
            return export_MovieType(request, config)
        elif table_name == 'Admin':
            return export_Admin(request, config)
        elif table_name == 'User':
            return export_User(request, config)
        elif table_name == 'Order':
            return export_Order(request, config)
        else:
            return Response.error('需提供表名')
