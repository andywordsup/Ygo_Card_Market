# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-11-13 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='商品名稱')),
                ('id_num', models.CharField(max_length=32, verbose_name='商品編號')),
                ('amount', models.IntegerField(verbose_name='商品數量')),
                ('price', models.CharField(max_length=11, verbose_name='price')),
                ('sort', models.EmailField(max_length=32, verbose_name='類別')),
                ('deal', models.IntegerField(verbose_name='交易次數')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(upload_to='avatar/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
