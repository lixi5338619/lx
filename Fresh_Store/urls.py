"""Fresh_Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from Buyer.urls import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('seller/',include("Seller.urls")),
    path('buyer/',include("Buyer.urls")),
    path('ckeditor',include('ckeditor_uploader.urls')),

    # path('^$',include("Buyer.urls"),
]
urlpatterns+=[
    re_path('^$', index),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('register_email/', register_email),
]


from Seller.views import GoodsApi
from Seller.views import example

urlpatterns += [
    path('Api/goods/', GoodsApi.as_view()),
    path('Api/example/', example),
    path('callbackPay/', callbackPay),
    re_path('paymethod/(\d+)', paymethod),
]