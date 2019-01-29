from django.urls import  path,re_path
from Buyer.views import *

urlpatterns =[
    re_path('^$', index),
    path('index/', index),
    path('sendMail/', sendMessage),
    # path('phone_zhuce/', phone_zhuce),
    re_path('goods_details/(?P<id>\d+)/', goods_details),
    re_path('carJump/(?P<goods_id>\d+)/', carJump),
    re_path('carList/', carList),
    re_path('delete_goods/(?P<goods_id>\d+)', delete_goods),
    re_path('clear_goods/', clear_goods),
    path('enter_order/', add_order),
    path('address/', address),
    path('addAddress/', addAddress),
    re_path('changeAddress/(?P<address_id>\d+)/', changeAddress),
    re_path('delAddress/(?P<address_id>\d+)/', delAddress),

    # path('Zhifubao_pay',Zhifubao_pay),

    path('openstore/', openstore),

    path('tiaozhuan', tiaozhuan),



    path('all_store/',all_store),
    path('conment/', conment),
    path('goods_details/', goods_details),
    path('goods_type/',goods_type),

    path('order_list/', order_list),
    path('orderdetail/', orderdetail),
    path('store_detail/', store_detail),
    path('user_center/', user_center),
    path('welcome/', welcome),
    path('base/', base),

    # path('register/', register),
]




handler404 = 'Buyer.views.page_not_found'
handler500 = "Buyer.views.page_error"