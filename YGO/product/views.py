import json
from datetime import datetime

from product.function_to_views import \
    save_pro, hand_pro, get_pros, \
    get_private_pros, check_del_info, \
    do_delete_pro

from django.http import JsonResponse
# Create your views here.
from tools.login_check import login_check
import time


@login_check('POST')
def products(request, username):
    # 在訪客的狀態不需要登入即可訪問商品
    if username == None:
        pass
    if request.method == 'GET':
        # 取得所有商品
        market_pros = get_pros()
        if isinstance(market_pros, dict):
            return JsonResponse(market_pros)
        # 商品資訊
        result = make_topics_res(market_pros)
        return JsonResponse(result)

    if request.method == "POST":
        request.META.get('HTTP_AUTHORIZATION')
        # 在裝飾器已經崁入user進request,藉由login_check(這是補充說明
        json_str = request.body
        if not json_str:
            return JsonResponse({'code': 201, 'error': 'Json is None'})
        json_obj = json.loads(request.POST.get('data'))
        file = request.FILES

        # 檢查上架商品資訊
        hand_info = hand_pro(request, json_obj, file)
        if isinstance(hand_info, dict):
            return JsonResponse(hand_info)
        # 檢查成功後執行存儲動作
        result = save_pro(request, file, hand_info)
        return JsonResponse(result)
    pass


@login_check('GET', 'DELETE')
def private_pro(request, username):
    # DELETE請求所需的迴避
    if username is None:
        pass
    if request.method == 'GET':

        # 取得私人上架過的商品
        private_pros = get_private_pros(request)
        if isinstance(private_pros, dict):
            return JsonResponse(private_pros)
        # 商品細項
        result = make_topics_res(private_pros)
        return JsonResponse(result)
    elif request.method == 'DELETE':
        # token = make_token(username)
        user = request.user.username
        # print('request.user:', user)
        # print('request.url:', url)
        # print('username:', username)
        # !!!!
        # 核對刪除訊息
        del_pro_data = check_del_info(request, user, username)
        if isinstance(del_pro_data, dict):
            return JsonResponse(del_pro_data)
        # !!!執行刪除
        result = do_delete_pro(del_pro_data)

        return JsonResponse(result)


# 商品細項
def make_topics_res(products):
    """
    products:資料群對象
    res{'code':200,'data':{[product obj],product obj}}
    product obj:
    :param author:被訪問者
    :param topics:
    :return:
    """

    res = {'code': 200, 'data': {}}
    data = {}
    products_list = []
    print('topics in make_topics_res:', products)
    # <QuerySet [<Topic: Topic object>, <Topic: Topic object>, <Topic: Topic object>]>
    for product in products:
        """
        """
        # 給的變量千萬不要是對象
        d = {}
        d['id'] = product.id
        # d['avatar'] = json.dumps(str(product.avatar))
        d['avatar'] = str(product.avatar)
        d['sort'] = product.sort
        d['title'] = product.title
        d['id_num'] = product.id_num
        d['price'] = product.price
        d['amount'] = product.amount
        d['created_time'] = product.created_time.strftime('%Y-%m-%d %H:%M:%S')
        products_list.append(d)
    data['products'] = products_list[::-1]
    res['data'] = data
    return res
