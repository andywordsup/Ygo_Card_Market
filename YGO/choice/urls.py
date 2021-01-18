from django.conf.urls import url, include

from choice import views

urlpatterns = [
    # 127.0.0.1:8000
    url(r'^', views.choice),
]