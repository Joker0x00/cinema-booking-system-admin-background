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


class Admin(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    role = models.CharField(max_length=11)

    class Meta:
        db_table = 'admin'


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    score = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    comments = models.CharField(max_length=700, blank=True, null=True)
    from_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

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


class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    show_id = models.CharField(max_length=255, blank=True, null=True)
    choose_seat = models.CharField(max_length=1024, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'order'


class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    seat_layout = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'room'


class Show(models.Model):
    field_id = models.CharField(db_column=' id', primary_key=True,
                                max_length=128)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    movie_id = models.CharField(max_length=255)
    room_id = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'show'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'user'
