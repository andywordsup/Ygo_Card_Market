import json
import re
from datetime import datetime

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


# 驗證後將商品送進購物車
def into_cart(json_obj):
    try:
        cid = json_obj.get('id')
        # print('==================================cid:', cid)
    except:
        return {'code': 213, 'error': 'NO_cid'}
    try:
        title = json_obj.get('title')
        # print('==================================title:', title)
    except:
        return {'code': 213, 'error': 'NO_tt'}
    try:
        id_num = json_obj.get('id_num')
        # print('==================================id_num:', id_num)
    except:
        return {'code': 213, 'error': 'NO_num'}
    try:
        price = json_obj.get('price')
        # print('==================================price:', price)
    except:
        return {'code': 213, 'error': 'NO_pp'}
    return [cid, title, id_num, price]


# 確認商品及數量
def sure_pro_info_buy_amount(into_cart_data, json_obj):
    cid = into_cart_data[0]
    try:
        car_pro = Product.objects.get(id=cid, amount__gt=0)
    except Exception as e:
        return JsonResponse({'code': 233, 'error': '商品已被通知即將下架'})
    # 這裡處理一下購買方案
    try:
        buy_amount = json_obj.get('buy_amount')
        if buy_amount is None:
            buy_amount = '1'
            return buy_amount
    except:
        buy_amount = '1'
        return buy_amount


# 存進購物車(創建商品data
def create_data_into_cart(request, into_cart_data, buy_amount):
    cid = into_cart_data[0]
    title = into_cart_data[1]
    id_num = into_cart_data[2]
    price = into_cart_data[3]
    try:
        car_ori = PayCar.objects.get(title=title, pro_id=cid, id_num=id_num, price=price,
                                     author=request.user)
        car_ori.buy_amount = int(car_ori.buy_amount) + int(buy_amount)
        car_ori.save()
        result = ({'code': 200, 'error': 'success'})
        return result


    except:
        try:
            car_pro = Product.objects.get(id=cid, amount__gt=0)
            print('buy_amount:', buy_amount)

            new_car_pro = PayCar.objects.create(title=title, pro_id=cid, id_num=id_num, price=price,
                                                buy_amount=int(buy_amount),
                                                author=request.user, market=car_pro)
        except Exception as e:
            raise
            # return JsonResponse({'code': 202, 'error': 'server save error'})
        try:
            new_car_pro.avatar = car_pro.avatar
            new_car_pro.save()

        except:
            raise
        result = ({'code': 200, 'error': 'success'})
        return result


# !!#確認修改內容
def check_info_to_ch(json_obj):
    if 'buy_amount' not in json_obj:
        return {'code': 207, 'error': 'buy_amount'}
    if 'id' not in json_obj:
        return {'code': 207, 'error': 'no id'}
    buy_amount = json_obj.get('buy_amount', '')
    car_id = json_obj.get('id', '')
    # print(car_id, buy_amount)
    # int(buy_amount)
    # str(car_id)
    try:
        car_pro = PayCar.objects.get(id=car_id)
        return [buy_amount, car_id, car_pro]
    except:
        # raise
        return {'code': 202, 'error': 'db no this product'}


# 確認移出的商品
def check_cancel_pro(url):
    try:
        car_pro = PayCar.objects.get(id=url)
        # '<li class="delete" style="padding-left:20px" data=' + topics[t].id +'>删除</li>';
        return car_pro
    except:
        return {'code': 318, 'error': 'cant get data!'}


# author_id: root(url傳的),跟後端使用這確認是否相同
# 透過外鍵確認
def check_author(car_pro, request):
    if car_pro.author.id != request.user.id:
        return {'code': 311, 'error': 'cant user.id:!! '}


def del_pro_in_db(car_pro):
    try:
        car_pro.delete()
        res = {'code': 200}
        return res
    except:

        raise


# 透過購物車紀錄去找商品剩餘數量
def find_db_date(checked_info):
    buy_amount = checked_info[0]
    car_id = checked_info[1]
    car_pro = checked_info[2]
    try:  # 透過購物車紀錄去找商品剩餘數量

        pro_id = car_pro.pro_id
        pro = Product.objects.get(id=pro_id, amount__gte=int(buy_amount))

    except:
        res = {'code': 277, 'data': {}, 'error': '購物車數量超出'}
        data = {}
        re_amount = []
        # raise
        pro = Product.objects.get(id=pro_id)
        amount = pro.amount
        re_amount.append(amount)
        data['re_amount'] = re_amount
        res['data'] = data
        return res


# !!存取修改內容
def save_check_info_in_db(checked_info):
    buy_amount = checked_info[0]
    car_pro = checked_info[2]
    try:
        car_pro.buy_amount = int(buy_amount)
        car_pro.save()
        result = {'code': 200, 'error': 'success'}
        return result
    except:
        return {'code': 202, 'error': 'server error'}


# 資料庫取出購物車購買商品
def get_pros_in_db(request):
    try:
        car_pros = PayCar.objects.filter(author=request.user.id)  # 購買者id
        # <QuerySet [<PayCar: PayCar object>, <PayCar: PayCar object>]>
        info = {}
        car_pros_list = []
        # [<QuerySet [<PayCar: PayCar object>, <PayCar: PayCar object>]>]

        for i in car_pros:
            f = {}
            f['id'] = i.id
            f['pro_id'] = i.pro_id  # 購物車中對應商品項目的pro_id
            f['title'] = i.title
            f['buy_amount'] = i.buy_amount  # 購買數量
            car_pros_list.append(f)
            info['car_pros'] = car_pros_list
        return info['car_pros']
    except:
        res = {'code': 600, 'error': 'no pro in cart '}
        return res


# 此循環驗證有無超出數量
def check_buy_amount(car_info):
    num = 0
    for i in car_info:
        pid = car_info[num]['id']
        print("+++++++++++++++", pid)
        pro_id = car_info[num]['pro_id']
        print("+++++++++++++++", pro_id)
        title = car_info[num]['title']
        print("+++++++++++++++", title)
        buy_amount = car_info[num]['buy_amount']
        print("+++++++++++++++", buy_amount)
        num += 1
        try:
            pro = Product.objects.get(id=pro_id)
            print('取商品核對')
            amount = pro.amount
        except:
            res = {'code': 311, 'error': 'match error '}
            print('核對失敗')
            return res
        if amount >= buy_amount:
            print('核對數量成功進行操作')
            pass
        else:
            print('核對數量超出存貨進行操作')
            res = {'code': 400, 'data': {}}
            data = {}
            error_pro_list = []
            error_pro = {'pro_id': pro_id, 'title': title, 'amount': amount}
            error_pro_list.append(error_pro)
            data['error_pro'] = error_pro_list
            res['data'] = data
            print("!!!!!!!!!!!!", pro_id, title, amount)
            return res


# 驗證無超出數量進入此循環購買
def into_purchase_procedure(car_info, username):
    num2 = 0
    ms_ms = ""
    for i in car_info:
        pid = car_info[num2]['id']
        print("+++++++++++++++", pid)
        pro_id = car_info[num2]['pro_id']
        print("+++++++++++++++", pro_id)
        title = car_info[num2]['title']
        print("+++++++++++++++", title)
        buy_amount = car_info[num2]['buy_amount']
        print("+++++++++++++++", buy_amount)
        num2 += 1
        try:
            pro = Product.objects.get(id=pro_id)
            print('取商品核對')
            amount = pro.amount
            amount = amount - int(buy_amount)
            print('扣除數量成功')
            pro.amount = amount
            pro.save()
            print('成功改變商品項目剩餘參數')
            del_pay = PayCar.objects.get(id=pid, pro_id=pro_id)
            print('取出要刪除的購物車商品')
            del_pay.delete()
            print('刪除購物車商品:', title)
            print('商品結帳成功數據為:%s,購買數量:%d:' % (title, buy_amount))
            ms: str = '商品結帳成功數據為:%s,購買數量:%d\n' % (title, buy_amount)
            ms_ms += ms
            try:
                user = UserProfile.objects.get(username=username)
                business_deal = user.business_deal
                business_deal = business_deal + 1
                user.business_deal = business_deal
                user.save()
                print('紀錄交易成功')
            except:
                print('紀錄交易失敗,聯絡官方')

        except:
            res = {'code': 333, 'error': '購買失敗聯絡官方 '}
            print('核對失敗,購買失敗聯絡官方')
            return res
    print("+++++++ms_ms", ms_ms)
    return ms_ms


# email function
def send_email(username, ms_ms):
    user = UserProfile.objects.get(username=username)
    try:
        print("into email")
        import email.message
        # 計送email程式
        # email寄送訊息物件設定
        try:
            em = user.email
        except Exception:
            raise
        msg = email.message.EmailMessage()
        print('msg = email.message.EmailMessage() 成功')
        msg["From"] = "andywordsup@gmail.com"
        # 這裡是變量
        msg["To"] = em
        print('em', em)
        msg["Subject"] = "訂單通知"
        msg.set_content(ms_ms)
        print('ms_ms', ms_ms)
        # msg.add_alternative("\'ms_ms\'", subtype="HTML")
        import smtplib
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("andywordsup@gmail.com", "gimjvgqnanadbmlv")
        server.send_message(msg)
    except:
        res = {'code': 465, 'error': '郵寄失敗聯絡官方 '}
        print('購買成功,郵寄失敗聯絡官方')
        return res
