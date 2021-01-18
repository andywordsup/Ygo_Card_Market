from django.conf.urls import url, include
from django.contrib import admin

from YGO import settings
from . import views

from django.conf.urls.static import static

urlpatterns = [
    # 127.0.0.1:8000
    url(r'^$', views.users),
    url(r'^/(?P<username>[\w]{1,11})$', views.users),
    # http://127.0.0.1:8000/v1/users/<username>
    # APPEND_SLASH 自动补全url后面的斜线，前提是你有一个 带 /的
    # 路由
]
