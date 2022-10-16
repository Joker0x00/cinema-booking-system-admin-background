# Author: wy
# Time: 2022/9/21 17:22
from . import rawSQL
import datetime


def validateShowTime(room_id, start_time, end_time, show_id=None):
    sql = """
        SELECT
            `show`.id AS show_id, 
            `show`.start_time AS start_time, 
            movie.length AS movie_length, 
            room.id AS room_id
        FROM
            `show`
            INNER JOIN
            movie
            ON 
                `show`.movie = movie.id
            INNER JOIN
            room
            ON 
                `show`.room = room.id
        WHERE `room`.`id` = %s
    """
    shows = rawSQL.query_all_dict(sql, (room_id,))
    for show in shows:
        if show_id == show['show_id']:
            continue
        st = show['start_time']
        ed = st + datetime.timedelta(minutes=show['movie_length'])
        if st <= start_time <= ed or st <= end_time <= ed:
            print('改放映时间已被占用')
            return False
        else:
            print('ok')
    return True
