from django.db import models

# Create your models here.
"""
買家帳號:
id account pwd nickname email phone 交易次數 收貨地址 avatar
"""


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用戶帳戶')
    password = models.CharField(max_length=32, verbose_name='用戶密碼')
    nickname = models.CharField(max_length=11, verbose_name='暱稱')
    address = models.CharField(max_length=50, verbose_name='收貨地址')
    email = models.EmailField(max_length=32, verbose_name='email')
    phone = models.CharField(max_length=32, verbose_name='連絡電話')
    business_deal = models.IntegerField(verbose_name='交易次數')
    # models.ImageField 存處的是圖片上的相對路徑並非直接存進去
    avatar = models.ImageField(upload_to='avatar/')

    class Meta:
        db_table = 'user_profile'
