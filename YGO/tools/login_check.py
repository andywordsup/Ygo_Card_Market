import jwt
from django.http import JsonResponse
from user.models import UserProfile

KEY = '1234567'


def login_check(*methods):
    """
    token驗正 HTTP://<username>
    :param method: 請求方法
    :return:
    """

    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            if request.method not in methods:
                return func(request, *args, **kwargs)
            # token is okay 直接傳回
            if not token:
                # result = {'code': 107, 'error': 'token error'}
                # return JsonResponse(result)
                raise
            try:
                # 網頁上取的要做調整,要再回來看
                res = jwt.decode(token, KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # token 過期a
                result = {'code': 107, 'error': 'login again'}
                return JsonResponse(result)
            except Exception as e:
                result = {'code': 108, 'error': 'login again'}
                return JsonResponse(result)
            username = res['username']
            try:
                user = UserProfile.objects.get(username=username)
            except:
                user = None
            if not user:
                result = {'code': 110, 'error': 'no user'}
                return JsonResponse(result)
            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    return _login_check
