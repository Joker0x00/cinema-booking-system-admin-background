# Author: wy
# Time: 2022/9/4 20:52
from django.views import View
from app import modelViews
from app.models import Show, Movie, Room
import json
import uuid
from django.db import connection
from app.utils.Pageination import Pagination
from django.http import JsonResponse
from app.utils.loadData import LoadJsonData
from app.utils.response import Response
from app.utils import select

class ShowView(View):
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
        print(condition)
        raw_data = modelViews.ShowView.objects.filter(**condition).values()
        raw_data = list(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取放映信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        print(form)
        movie_id = form['movie_id']
        movie_obj = Movie.objects.filter(id=movie_id).first()
        room_id = form['room_id']
        room_obj = Room.objects.filter(id=room_id).first()
        obj = Show(
            id=uuid.uuid1(),
            movie_id=movie_obj,
            room_id=room_obj,
            start_time=form['start_time'],
            price=form['price']
        )
        obj.save()
        return Response.success(message='新增成功')

    def put(self, request):
        raw_form = LoadJsonData(request.body).get_data().get('form', {})
        form = {
            'id': raw_form.get('id', ''),
            'movie_id': raw_form.get('movie_id', ''),
            'room_id': raw_form.get('room_id', ''),
            'start_time': raw_form.get('start_time', ''),
            'price': raw_form.get('price', ''),
        }
        # 数据验证和处理
        movie_obj = Movie.objects.filter(id=form['movie_id']).first()
        room_obj = Room.objects.filter(id=form['room_id']).first()
        show_obj = Show.objects.filter(id=form['id']).first()
        show_obj.movie_id = movie_obj
        show_obj.room_id = room_obj
        show_obj.start_time = form['start_time']
        show_obj.seat_layout = form['seat_layout']
        show_obj.price = form['price']
        show_obj.save()

        return JsonResponse(Response(code=200, success=True, message='修改成功').normal())

    def delete(self, request):
        showId = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Room id:' + showId)
        if not showId:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        obj = Show.objects.filter(id=showId).first()
        if not obj:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        obj.delete()
        return Response(code=200, success=True, message='删除成功').jsonResponse()
