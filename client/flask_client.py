# -*- coding:utf-8 -*-
######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
#     > Mail: 250919354@qq.com
#     > Created Time: Mon 20 May 2019 11:52:00 AM CST
######################################################

from flask import Flask, send_file

app = Flask(__name__)

@app.route('/test2')
def test2():
    # 首页未登入測試
    return send_file('templates/test2.html')

@app.route('/login')
def login():
    # 登入
    return send_file('templates/login.html')


@app.route('/register')
def register():
    # 註冊
    return send_file('templates/register.html')
    
@app.route('/<username>/testinto')
def testinto(username):
    # 首页登入入測試
    return send_file('templates/test_into.html')
    
@app.route('/<username>/paycar')
def paycar(username):
    # 首页登入入測試
    return send_file('templates/paycar.html')
        
@app.route('/<username>/car_info')
def car_info(username):
    # 首页登入入測試
    return send_file('templates/car_info.html')

@app.route('/<username>/product')
def product(username):
    # 商品上架頁面
    return send_file('templates/products.html')

@app.route('/<username>/product2')
def product2(username):
    # 商品上架頁面
    return send_file('templates/products2.html')

@app.route('/<username>/market')
def market(username):
    # 
    return send_file('templates/market.html')
    
@app.route('/index')
def index():
    # 
    return send_file('templates/index.html')




@app.route('/<username>/self')
def self(username):
    # 個人資料頁面
    return send_file('templates/self.html')


@app.route('/new_index')
def new_index(): 
    return send_file('templates/new_index.html')

@app.route('/<username>/new_del_pro')
def new_del_pro(username):
    return send_file('templates/new_del_pro.html')


@app.route('/<username>/shopping_cart')
def shopping_cart(username):
    # 
    return send_file('templates/shopping_cart.html')


@app.route('/<username>/new_self')
def new_self(username):
    # 個人資料頁面
    return send_file('templates/new_self.html')

if __name__ == '__main__':
    app.run(debug=True)
