import json
import re
from datetime import datetime

from paycar.function_to_views import \
    into_cart, sure_pro_info_buy_amount, \
    create_data_into_cart, check_info_to_ch, \
    find_db_date, save_check_info_in_db, \
    get_pros_in_db, check_buy_amount, into_purchase_procedure, send_email, check_cancel_pro, check_author, del_pro_in_db
from paycar.models import PayCar
from product.models import Product
from django.http import JsonResponse
from django.shortcuts import render
import os
# Create your views here.
from tools.login_check import login_check
import html
import time

from user.models import UserProfile
from user.views import make_token


@login_check('POST', 'DELETE')
def paycar(request, username):
    if username == "":
        pass
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        return JsonResponse({'code': 313, 'error': 'no user'})

    if request.method == "GET":
        try:
            car_pros = PayCar.objects.filter(author_id=user.id)
        except Exception as e:
            return JsonResponse({'code': 313, 'error': 'no topic'})
        result = make_car_res(car_pros)
        return JsonResponse(result)

    if request.method == "POST":
        # request.META.get('HTTP_AUTHORIZATION')
        # 獲取 json對象
        json_str = request.body
        if not json_str:
            return JsonResponse({'code': 201, 'error': 'Json is None'})
        # 轉成python對象
        json_obj = json.loads(json_str)
        # !!!驗證後將商品送進購物車
        into_cart_data = into_cart(json_obj)
        if isinstance(into_cart_data, dict):
            return JsonResponse(into_cart_data)
        # 確認商品及數量
        buy_amount = sure_pro_info_buy_amount(into_cart_data, json_obj)
        if isinstance(buy_amount, dict):
            return JsonResponse(buy_amount)
        # 存進購物車(創建商品data
        result = create_data_into_cart(request, into_cart_data, buy_amount)

        return JsonResponse(result)

    if request.method == "PUT":
        json_str = request.body
        if not json_str:
            return JsonResponse({'code': 201, 'error': 'Json is None'})
        # 轉成python對象
        json_obj = json.loads(json_str)
        # !!#確認修改內容
        checked_info = check_info_to_ch(json_obj)
        if isinstance(checked_info, dict):
            return JsonResponse(checked_info)

        # 透過購物車紀錄去找商品剩餘數量
        db_date = find_db_date(checked_info)
        if isinstance(db_date, dict):
            return JsonResponse(db_date)
            # raise
        # !!存取修改內容
        result = save_check_info_in_db(checked_info)
        return JsonResponse(result)

    if request.method == "DELETE":
        # token = make_token(username)
        user = request.user.username
        url = request.GET.get('did')
        # print("url:", url)
        if url == "buy":
            result = payment(request, username)
            return JsonResponse(result)
        else:
            # print('request.user:', user)
            # print('request.url:', url)
            # print('username:', username)
            if user != username:
                result = {'code': 309, 'error': 'go to login again '}
                return JsonResponse(result)
            # 確認移出的商品
            car_pro = check_cancel_pro(url)
            if isinstance(car_pro, dict):
                return JsonResponse(car_pro)

            # author_id: root(url傳的),跟後端使用這確認是否相同
            # 透過外鍵確認
            ch_error = check_author(car_pro, request)
            if isinstance(ch_error, dict):
                return JsonResponse(ch_error)
            # 商品從資料庫刪除
            res = del_pro_in_db(car_pro)

            return JsonResponse(res)


# 預購項目
def make_car_res(car_pros):
    """
    products:資料群對象
    res{'code':200,'data':{[product obj],product obj}}
    product obj:
    :param author:被訪問者
    :param topics:被訪問者文章
    :return:
    """

    res = {'code': 200, 'data': {}}
    data = {}
    car_pros_list = []
    print('topics in make_topics_res:', car_pros)
    # <QuerySet [<Topic: Topic object>, <Topic: Topic object>, <Topic: Topic object>]>
    for car_pro in car_pros:
        """

        """
        # 給的變量千萬不要是對象
        d = {}
        d['id'] = car_pro.id
        # d['avatar'] = json.dumps(str(car_pro.avatar))
        d['avatar'] = str(car_pro.avatar)
        d['sort'] = car_pro.sort
        d['title'] = car_pro.title
        d['id_num'] = car_pro.id_num
        d['price'] = car_pro.price
        d['buy_amount'] = car_pro.buy_amount
        d['created_time'] = car_pro.created_time.strftime('%Y-%m-%d %H:%M:%S')
        # d['lave']=car_pro.
        car_pros_list.append(d)
    data['car_pros'] = car_pros_list[::-1]
    res['data'] = data
    return res


# 進行結帳
def payment(request, username):
    print("進入def payment")
    user = request.user.username
    if user != username:
        res = {'code': 309, 'error': 'go to login again '}
        return res
    try:
        # 資料庫取出購物車購買商品
        car_info = get_pros_in_db(request)
        if isinstance(car_info, dict):
            return car_info
        # 此循環驗證有無超出數量
        error_amount = check_buy_amount(car_info)
        if isinstance(error_amount, dict):
            return error_amount
        # 驗證無超出數量進入此循環購買
        ms_ms = into_purchase_procedure(car_info, username)
        if isinstance(ms_ms, dict):
            return ms_ms
        # email function
        send_error = send_email(username,ms_ms)
        if isinstance(send_error, dict):
            return send_error
        # 回傳
        res = {'code': 200}
        print('完成結帳!!!!')
        return res
    except:
        res = {'code': 600, 'error': 'no pro in cart '}
        return res
