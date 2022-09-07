# Author: wy
# Time: 2022/8/30 21:35
from django.db import models


class MovieView(models.Model):
    id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci', primary_key=True)
    name = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci')
    category = models.IntegerField(blank=True, null=True)
    stars = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    info = models.CharField(max_length=1000, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    image = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    location = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    movietypename = models.CharField(db_column='movieTypeName', max_length=128, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)  # Field name made lowercase.
    movietypeid = models.IntegerField(db_column='movieTypeId')  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'moive_view'

from django.db import models


class ShowView(models.Model):
    id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci', primary_key=True)
    movie_id = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci')
    moviename = models.CharField(db_column='movieName', max_length=255, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    length = models.IntegerField(blank=True, null=True)
    room_id = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci')
    roomname = models.CharField(db_column='roomName', max_length=255, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    size = models.IntegerField()
    seat_layout = models.CharField(max_length=1000, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    column = models.IntegerField()
    row = models.IntegerField()
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'show_view'


class OrderDetail(models.Model):
    id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci', primary_key=True)
    moviename = models.CharField(db_column='movieName', max_length=255, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    show_id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci')
    choose_seat = models.CharField(max_length=1024, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    user_id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci')
    username = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci')
    create_time = models.DateTimeField(blank=True, null=True)
    roomname = models.CharField(db_column='roomName', max_length=255, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    room_id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci')
    movie_id = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    num = models.IntegerField(default=0)
    status = models.CharField(max_length=30)
    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'order_detail'