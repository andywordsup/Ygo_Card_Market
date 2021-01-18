# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-10-13 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='用戶帳戶')),
                ('password', models.CharField(max_length=32, verbose_name='用戶密碼')),
                ('nickname', models.CharField(max_length=11, verbose_name='暱稱')),
                ('address', models.CharField(max_length=50, verbose_name='收貨地址')),
                ('email', models.EmailField(max_length=32, verbose_name='email')),
                ('phone', models.CharField(max_length=32, verbose_name='連絡電話')),
                ('business_deal', models.IntegerField(verbose_name='交易次數')),
                ('avatar', models.ImageField(upload_to='avatar/')),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]