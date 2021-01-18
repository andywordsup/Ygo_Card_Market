import hashlib
import json
import time
from django.db.models import Avg, Sum, Max, Min
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from tools.login_check import login_check
from user.functions_to_views import \
    check_account, create_ch, check_repeat_username, \
    save_change_info, hash_pwd, create_account, check_have_user_not
from user.models import UserProfile


@login_check('PUT')
def users(request, username=None):
    if request.method == 'GET':
        # 檢查是否有用戶登入
        user = check_have_user_not(username)
        # 驗證帳號密碼是否正確
        result = check_account(request, username, user)
        return JsonResponse(result)


    elif request.method == 'POST':
        json_str = request.body
        # 把字串改成python對象
        json_obj = json.loads(json_str)
        # 檢查帳號密碼
        user_info = create_ch(json_obj)
        # 回傳字典格式表示失敗
        if isinstance(user_info, dict):
            return JsonResponse(user_info)
        # 接下來檢查用戶名是否重複
        already_check_info = check_repeat_username(user_info)
        # 哈希加密
        hash_info = hash_pwd(already_check_info)
        # 產生帳號
        create_account(hash_info)
        token = make_token(hash_info[0])
        result = {'code': 200, 'username': hash_info[0], 'data': {'token': token.decode()}}
        return JsonResponse(result)



    elif request.method == 'PUT':
        # 修改用戶數據
        request.META.get('HTTP_AUTHORIZATION')
        # 在裝飾器已經崁入user進request
        user = request.user
        # 前端下來信息 一定是字串
        json_str = request.body
        # 取得json_str訊息 修改資料
        result = save_change_info(request, json_str)
        return JsonResponse(result)
    else:
        return JsonResponse({'code': 211, 'error': 'error request'})


# 成功則給token
def make_token(username, expire=3600 * 36):
    """
    創建成功則給token
    :param username:
    :param expire:
    :return:
    """
    import jwt
    key = '1234567'
    now = time.time()
    payload = {'username': username, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')
