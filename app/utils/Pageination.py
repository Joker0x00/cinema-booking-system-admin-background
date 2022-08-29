# Author: wy
# Time: 2022/8/27 20:46
class Pagination(object):
    def __init__(self, current_page, limit, count):
        try:
            current_page = int(current_page)
            limit = int(limit)
        except Exception as e:
            current_page = 1
            limit = 10
            count = count
        # print(current_page)
        # print(limit)

        self.current_page = current_page if current_page >= 1 else 1
        self.count = count
        self.limit = limit if limit >= 1 else 1
        # 总页码
        all_pager, tmp = divmod(count, limit)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

    def get_result(self):
        # print(self.current_page)
        # print(self.limit)
        # print(self.count)
        start = (self.current_page - 1) * self.limit
        end = self.current_page * self.limit
        return start, end
