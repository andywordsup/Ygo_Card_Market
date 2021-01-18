import hashlib
import json
import time
from django.db.models import Avg, Sum, Max, Min
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from tools.login_check import login_check
from user.models import UserProfile


def check_have_user_not(username):
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        user = None
        return user
    return user


# 驗證帳號密碼是否正確
def check_account(request, username, user):
    """

    :param request: 請求類型
    :param username: 字段
    :param user: object
    :return:
    """
    if not user:
        result = {'code': 208, 'error': 'no user'}
        return result
    if request.GET.keys():
        # 查询指定字段
        data = {}
        for k in request.GET.keys():
            if hasattr(user, k):
                v = getattr(user, k)
                if k == 'avatar':
                    data[k] = str(v)
                else:
                    data[k] = v
        result = {'code': 200, 'username': username, 'data': data}
        return result
    else:
        result = {'code': 200, 'username': username,
                  'data': {'email': user.email, 'phone': user.phone, 'address': user.address,
                           'business_deal': user.business_deal}}
        return result


#   創建用戶檢查帳號密碼
def create_ch(json_obj):
    """

    :param username: POST 提交的用戶名
    :param json_obj:
    :return:
    """
    username = json_obj.get('username')
    if not username:
        res = {'code': 202, 'error': 'enter error'}
        return res
    email = json_obj.get('email')
    if not email:
        res = {'code': 203, 'error': 'enter error'}
        return res
    password_1 = json_obj.get('password_1')
    password_2 = json_obj.get('password_2')
    if not password_1 or not password_2:
        res = {'code': 204, 'error': 'enter error'}
        return res
    if password_1 != password_2:
        res = {'code': 205, 'error': 'enter pwd difference'}
        return res
    res = [username, email, password_1]
    return res


# 接下來檢查用戶名是否重複
def check_repeat_username(user_info):
    username = user_info[0]
    email = user_info[1]
    password_1 = user_info[2]
    old_user = UserProfile.objects.filter(username=username)
    if old_user:
        return {'code': 206, 'error': 'username already existed'}
    return [username, email, password_1]


# 密碼處理 md5 哈希
def hash_pwd(already_check_info):
    # 密碼處理 md5 哈希
    username = already_check_info[0]
    email = already_check_info[1]
    password_1 = already_check_info[2]
    m = hashlib.md5()  # 哈希事前動作
    m.update(password_1.encode())  # 哈希處理密碼
    # print('m', m)
    return [username, email, m]


# 產生帳號功能
def create_account(hash_info):
    username = hash_info[0]
    email = hash_info[1]
    m = hash_info[2]
    try:
        UserProfile.objects.create(username=username, password=m.hexdigest(), email=email, business_deal=0)
    except Exception as e:
        return JsonResponse({'code': 202, 'error': 'service is busy'})


# 修改資料
def save_change_info(request, json_str):
    info = []
    if not json_str:
        return {'code': 207, 'error': 'no json'}
    # 把字串改成python對象
    json_obj = json.loads(json_str)
    if 'email' not in json_obj:
        return {'code': 207, 'error': 'no email'}
    if 'phone' not in json_obj:
        return {'code': 207, 'error': 'no phone'}
    if 'address' not in json_obj:
        return {'code': 207, 'error': 'no address'}
    email = json_obj.get('email', '')
    phone = json_obj.get('phone', '')
    address = json_obj.get('address', '')
    # 存起來
    request.user.phone = phone
    request.user.email = email
    request.user.address = address
    request.user.save()
    result = {'code': 200, 'username': request.user.username}
    return result


# 創建成功則給token
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
