from django.shortcuts import render
from django.db import models
from product.models import Product
# Create your views here.
from django.http import JsonResponse
import html
import json
import time
from datetime import datetime
from product.views import make_topics_res


def choice(request):
    if request.method == 'GET':
        sort = request.GET.get('get_sort')
        if sort=="Show_All":
            now = time.time()
            try:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                products = Product.objects.filter(created_time__lt=now)
                # user in get: UserProfile object
            except Exception as e:
                raise
                # result = {'code': 408, 'error': 'server error '}
                # return JsonResponse(result)
                # 检查是否有查询字符串
            result = make_topics_res(products)
            return JsonResponse(result)
            pass
        else:
            products = Product.objects.filter(sort=sort)
            result = make_topics_res(products)
            return JsonResponse(result)

