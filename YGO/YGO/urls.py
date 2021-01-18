"""YGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from YGO import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/$', views.test_api),
    url(r'^v1/users', include('user.urls')),
    url(r'^v1/tokens', include('ytoken.urls')),
    url(r'^v1/products', include('product.urls')),
    url(r'^v1/choice', include('choice.urls')),
    url(r'^v1/paycar', include('paycar.urls')),

]
# 媒體資API
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)