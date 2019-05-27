# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey('TBooks', models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey('TOrder', models.DO_NOTHING, blank=True, null=True)
    book_number = models.IntegerField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'order_item'


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    column_8 = models.CharField(db_column='Column_8', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 't_address'


class TBooks(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    press = models.CharField(max_length=30, blank=True, null=True)
    press_time = models.DateTimeField(blank=True, null=True)
    edition = models.CharField(max_length=20, blank=True, null=True)
    printing_time = models.DateTimeField(blank=True, null=True)
    impression = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    number = models.CharField(max_length=20, blank=True, null=True)
    page_number = models.CharField(max_length=20, blank=True, null=True)
    format = models.CharField(max_length=20, blank=True, null=True)
    paper = models.CharField(max_length=20, blank=True, null=True)
    pack = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    dd_price = models.FloatField(blank=True, null=True)
    recommend = models.CharField(max_length=500, blank=True, null=True)
    introduce = models.CharField(max_length=200, blank=True, null=True)
    author_intro = models.CharField(max_length=200, blank=True, null=True)
    list = models.CharField(max_length=200, blank=True, null=True)
    reviews = models.CharField(max_length=200, blank=True, null=True)
    insert_map = models.CharField(max_length=500, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    shelf_time = models.DateTimeField(blank=True, null=True)
    route = models.CharField(max_length=50, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    is_sale = models.IntegerField(blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)
    sort = models.ForeignKey('TSort', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_books'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    tptal_price = models.FloatField(blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
     # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 't_order'


class TSort(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_sort'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    u_email = models.CharField(max_length=40, blank=True, null=True)
    u_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    has_confirm = models.BooleanField(default=False,verbose_name='是否确认')

    class Meta:
        # managed = False
        db_table = 't_user'

class Confirm_string(models.Model):
    code = models.CharField(max_length=256,verbose_name='用户注册码')
    user = models.ForeignKey('TUser',on_delete=models.CASCADE,verbose_name='关联的用户')
    code_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_confirm_string'