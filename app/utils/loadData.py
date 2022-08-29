# Author: wy
# Time: 2022/8/27 10:24
import json


class LoadJsonData:

    def __init__(self, body):
        self.data = json.loads(body)

    def get_data(self):
        return self.data
