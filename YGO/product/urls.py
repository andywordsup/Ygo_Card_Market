from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # 127.0.0.1:8000
    url(r'^$', views.products),
    # http://127.0.0.1:8000/v1/users/<username>
    # APPEND_SLASH 自动补全url后面的斜线，前提是你有一个 带 /的
    # 路由
    url(r'^/(?P<username>[\w]{1,11})$', views.products),
    # http://127.0.0.1:8000/v1/users/<username>/avatar
    url(r'^/(?P<username>[\w]{1,11})/avatar$', views.products),
    url(r'^/(?P<username>[\w]{1,11})/del', views.private_pro),

]
