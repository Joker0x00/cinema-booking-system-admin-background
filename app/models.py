from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class Admin(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    role = models.CharField(max_length=100)

    class Meta:
        db_table = 'admin'


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comments = models.CharField(max_length=700, blank=True, null=True)
    from_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField()
    movie = models.ForeignKey('Movie', models.DO_NOTHING)
    class Meta:
        db_table = 'comment'


class Movie(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255)
    category = models.ForeignKey('MovieType', models.DO_NOTHING, db_column='category', blank=True, null=True)
    stars = models.CharField(max_length=255, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    info = models.CharField(max_length=1000, blank=True, null=True)
    image = models.FileField(max_length=255, blank=True, null=True, upload_to='image/')
    location = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'movie'


class MovieType(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'movie_type'

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    show_id = models.ForeignKey('Show', models.DO_NOTHING, blank=True, null=True)
    choose_seat = models.CharField(max_length=1024, blank=True, null=True)
    user_id = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField()
    num = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)
    class Meta:
        db_table = 'order'


class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255)
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    offset = models.IntegerField(default=0)
    seat_layout = models.CharField(max_length=1000, blank=True, null=True)
    screen_width = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'room'


class Show(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    movie = models.ForeignKey('Movie', models.DO_NOTHING)
    room = models.ForeignKey('Room', models.DO_NOTHING)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_layout = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        db_table = 'show'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    sex = models.CharField(max_length=2, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'user'

