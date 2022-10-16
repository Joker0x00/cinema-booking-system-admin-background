# Author: wy
# Time: 2022/10/5 21:06
from app.utils import rawSQL
from app.utils.Pageination import Pagination
from app.utils.response import Response


def get_log(request):
    current_page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))
    sql = """
        select * from log
        order by log.`time` desc 
    """
    data = rawSQL.query_all_dict(sql)
    print(data)
    start, end = Pagination(current_page=current_page, limit=limit, count=len(data)).get_result()
    rows = data[start: end]
    data = {
        'count': len(data),
        'rows': rows,
    }
    return Response.success(data=data, message='获取日志成功')