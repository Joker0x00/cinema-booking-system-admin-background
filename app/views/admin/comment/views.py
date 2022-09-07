# Author: wy
# Time: 2022/9/7 19:43
import uuid

from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from app.utils import rawSQL
from app.utils.Pageination import Pagination
from app.utils.loadData import LoadJsonData
from app.utils.response import Response
from app.models import Comment
from app.modelViews import CommentDetail


class CommentView(View):
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
        # 1
        raw_data = CommentDetail.objects.filter(**condition).values()
        raw_data = list(raw_data)
        cnt = len(raw_data)
        start, end = Pagination(current_page=current_page, limit=limit, count=cnt).get_result()
        rows = raw_data[start: end]
        print(rows)
        data = {
            'count': cnt,
            'rows': rows,
        }
        return JsonResponse(Response(code=200, data=data, message='成功获取评论信息').normal(), safe=False)

    def post(self, request):
        form = LoadJsonData(request.body).get_data().get('form', {})
        score = form['score']
        comments = form['comments']
        user_id = form['user_id']
        sql = 'insert into `comment`' \
              '(id, score, comments, from_user, create_time) ' \
              'VALUES' \
              ' ("{}", "{}", "{}", "{}", "{}")'.format(uuid.uuid1(), score, comments,
                                                                         user_id, timezone.now())
        rawSQL.execSql(sql)
        return Response.success(message='新增成功')


    def delete(self, request):
        comment_id = LoadJsonData(request.body).get_data().get('id', '')
        print('Delete Type:Comment id:' + comment_id)
        if not comment_id:
            return Response(code=404, success=False, message='删除失败，id为空').jsonResponse()
        sql = 'select `id` from `comment` where `id`=%s'
        params = (comment_id,)
        data = rawSQL.query_one_dict(sql, params)
        if not data:
            return Response(code=404, success=False, message='删除失败，检索不到').jsonResponse()
        sql = 'delete from `comment` where `id`=%s'
        params = (comment_id,)
        rawSQL.execSql(sql, params)
        return Response(code=200, success=True, message='删除成功').jsonResponse()