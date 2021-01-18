from django.db import models
# Create your models here.
from user.models import UserProfile
from product.models import Product

"""
買家帳號:
	user_id(購買者帳號) /commodity_id 數量 

"""


class PayCar(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='存放編號')
    pro_id = models.CharField(max_length=32, verbose_name='商品正編product_id')
    title = models.CharField(max_length=32, verbose_name='商品名稱')
    id_num = models.CharField(max_length=32, verbose_name='商品編號')
    buy_amount = models.IntegerField(verbose_name='預計購買數量')
    price = models.CharField(max_length=11, verbose_name='price')
    sort = models.EmailField(max_length=32, verbose_name='類別')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # 外键
    author = models.ForeignKey(UserProfile)
    market = models.ForeignKey(Product)
    # models.ImageField 存處的是圖片上的相對路徑並非直接存進去
    avatar = models.ImageField(upload_to='avatar/')

    class Meta:
        db_table = 'paycar'

# Create your models here.
