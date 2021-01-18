from django.db import models

# Create your models here.
from user.models import UserProfile

"""
買家帳號:
id 名稱 商品編號 數量?  price 上架時間 訂單數量 類別

"""


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='商品名稱')
    id_num = models.CharField(max_length=32, verbose_name='商品編號')
    amount = models.IntegerField(verbose_name='商品數量')
    price = models.CharField(max_length=11, verbose_name='price')
    sort = models.EmailField(max_length=32, verbose_name='類別')
    deal = models.IntegerField(verbose_name='交易次數')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # 外键
    author = models.ForeignKey(UserProfile)
    # models.ImageField 存處的是圖片上的相對路徑並非直接存進去
    avatar = models.ImageField(upload_to='avatar/')

    class Meta:
        db_table = 'product'

# Create your models here.
