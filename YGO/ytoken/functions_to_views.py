import hashlib
import json
from django.http import JsonResponse
from user.models import UserProfile
from user.views import make_token


# 處理登入驗證產生token
def req_token_ch(request):
    json_str = request.body
    if not json_str:
        result = {'code': 102, 'error': 'Please give me json'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    username: object = json_obj.get('username')
    if not username:
        result = {'code': 102, 'error': 'not username'}
        return JsonResponse(result)
    password = json_obj.get('password')
    if not password:
        result = {'code': 102, 'error': 'not password'}
        return JsonResponse(result)

    user = UserProfile.objects.filter(username=username)
    if not user:
        result = {'code': 103, 'error': 'check '}
        return JsonResponse(result)
    user = user[0]  # because of filter
    m = hashlib.md5()
    m.update(password.encode())  # json 對象轉python
    if m.hexdigest() != user.password:
        result = {'code': 103, 'error': 'check '}
        return JsonResponse(result)
    token = make_token(username)

    res = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
    return res
