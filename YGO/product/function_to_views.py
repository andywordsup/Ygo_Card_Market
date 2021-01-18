import os
from product.models import Product
import html
from datetime import datetime



def get_pros():
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        products = Product.objects.filter(created_time__lt=now)
        # user in get: UserProfile object
        return products
    except Exception as e:
        # raise
        return {'code': 408, 'error': 'server error '}


# 檢查上架商品資訊
def hand_pro(request, json_obj, file):
    aurl = json_obj.get('aurl')
    if not aurl:
        return {'code': 777, 'error': 'url error'}
    t_id = aurl.split('/')[-1].split('/')[-1]
    user = request.user.username
    print('url_POST:', aurl)
    print('t_id_POST:', t_id)
    print('request.user:', user)  # ROOT
    if user != t_id:
        return {'code': 777, 'error': 'login again'}
    avatar = file
    if not avatar:
        return {'code': 202, 'error': 'enter avatar'}
    sort = json_obj.get('sort')
    if not sort:
        return {'code': 203, 'error': 'enter error'}
    title = json_obj.get('title')
    # 防止有人白目
    title = html.escape(title)
    if not title:
        return {'code': 204, 'error': 'enter error'}
    id_num = json_obj.get('id_num')
    if not id_num:
        return {'code': 205, 'error': 'enter error'}
    price = json_obj.get('price')
    if not price:
        return {'code': 206, 'error': 'enter error'}
    amount = json_obj.get('amount')
    if not amount:
        return {'code': 202, 'error': 'enter error'}
    pwd = json_obj.get('pwd')
    if not pwd or pwd != '111111':
        return {'code': 202, 'error': 'pwd no power'}
    res = [sort, title, id_num, price, amount]
    return res

# 檢查成功後執行存儲動作
def save_pro(request, file, hand_info):
    sort = hand_info[0]
    title = hand_info[1]
    id_num = hand_info[2]
    price = hand_info[3]
    amount = hand_info[4]
    try:

        Product.objects.create(sort=sort, title=title, id_num=id_num,
                               price=price, amount=int(amount), deal=0, author=request.user)

    except Exception as e:
        # raise
        return {'code': 202, 'error': 'server save error'}
    try:

        pr = Product.objects.get(sort=sort, title=title, id_num=id_num,
                                 price=price, amount=int(amount), deal=0, author=request.user)

    except Exception as e:
        return {'code': 202, 'error': 'server get obj error'}
    try:
        id = pr.id
        print('pr.id:', id)
        # pr.avatar=avatar
        pr.avatar = file.get('avatar')
        pr.avatar.save(str(id) + '.png', file.get('avatar'))
        pr.save()
    except Exception as e:
        return {'code': 202, 'error': 'avatar saved error'}
    result = {'code': 200, 'error': 'success'}
    return result


def get_private_pros(request):
    try:
        user = request.user
        id = user.id
        print('user.id:', id)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        products = Product.objects.filter(author_id=user.id, created_time__lt=now)
        # user in get: UserProfile object
        return products
    except Exception as e:
        return {'code': 408, 'error': 'visitor error '}
        # 检查是否有查询字符串


def check_del_info(request, user, username):
    if user != username:
        result = {'code': 309, 'error': 'go to login again '}
        return result
    try:
        # 透過字段判別刪除對象
        url = request.GET.get('did')
        # 有此商品
        product = Product.objects.get(id=url)
        # '<li class="delete" style="padding-left:20px" data=' + topics[t].id +'>删除</li>';
        # 透過外健檢查是否是本人上架的商品
        if product.author.id != request.user.id:
            result = {'code': 311, 'error': 'cant get data!! '}
            return result
        return product
    except:
        result = {'code': 318, 'error': 'cant get data!'}
        return result
    # # 删除 ex: author_id: root(url傳的),跟後端使用這確認是否相同

def do_delete_pro(del_pro_data):
    try:
        # 刪除後端文件夾中的圖檔
        fileimg = "media/" + str(del_pro_data.avatar)
        os.remove(fileimg)
        del_pro_data.delete()
        res = {'code': 200}
        return res
    except:
        return {'code': 339, 'error': 'delete error!'}

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
