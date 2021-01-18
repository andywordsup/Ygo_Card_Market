import hashlib

from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
from user.models import UserProfile

from user.views import make_token
from ytoken.functions_to_views import req_token_ch


# 登入時創建
def tokens(request):
    """
    創建token:login
    :param request: 請求
    :return: token
    """
    # 如果不是POST則回傳錯誤
    if request.method != 'POST':
        result = {'code': 101, 'error': 'go to login'}
        return JsonResponse(result)
    # 處理登入驗證產生token
    result = req_token_ch(request)
    return JsonResponse(result)
