from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

import json
import redis

from api import models
from api.utils.response import BaseResponse


# 全局配置
USER_ID = 1
redis_conn = redis.Redis(host="192.168.11.110",port=6379)

class ShoppingCarView(ViewSetMixin,APIView):


    def list(self, request, *args, **kwargs):
        """
        显示购物车内的内容
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 返回 课程，价格策略的数据
        #
        # redis_conn.set("age","18")
        # name =  redis_conn.get("age")
        # print(name)

        ret = {'code':10000,'data':None,'error':None}
        try:
            shopping_car_course_list = []
            # 使用模糊查询，获取该用户的所有课程
            patten = "shop_car_%s_%s" % (USER_ID, "*")

            user_key_list = redis_conn.keys(patten)

            for key in user_key_list:
                temp = {
                    'id': redis_conn.hget(key, 'id').decode('utf-8'),
                    'name': redis_conn.hget(key, 'name').decode('utf-8'),
                    'img':redis_conn.hget(key, 'img').decode('utf-8'),
                    'default_price_id':redis_conn.hget(key, 'default_price_id').decode('utf-8'),
                    'price_policy_dict': json.loads(redis_conn.hget(key, 'price_policy_dict').decode('utf-8'))
                }
                shopping_car_course_list.append(temp)

            ret['data'] = shopping_car_course_list
        except Exception as e:
            ret['code'] = 10005
            ret['error']  = '获取购物车数据失败'

        return Response(ret)



    def  create(self,request,*args,**kwargs):
        """
            将数据加入购物车
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        ret =  BaseResponse()

        # 1. 接受用户选中的课程ID和价格策略ID
        # 在view 视图中， request 被封装，数据在data内
        # get,方法进行反序列化， 将字符串转为数字
        course_id = request.data.get("courseid")
        price_id = request.data.get("priceid")

        print(course_id,price_id)

        # 2. 判断合法性
        #     - 课程是否存在？
        #     - 价格策略是否合法？

        # 课程是否合法
        course_obj = models.Course.objects.filter(id=course_id).first()
        if  not course_obj :
            ret.code= 1000
            ret.error="没有该课程"
            return Response(ret.dict)

        # 价格策略是否合法
        # 商品的周期，价格，id
        # 通过content_type 正向查询了，所有的价格价格策略对象
        course_price_query = course_obj.price_policy.all()
        course_price_policy_dict= {}
        for item in course_price_query:
            # 显示价格周期的所有数据
            ret2 = {
                'id' : item.id,
                'price' :item.price,
                'valid_period': item.valid_period,
                'valid_period_display': item.get_valid_period_display(),
            }
            course_price_policy_dict[item.id] = ret2

        print("ssssss",course_price_policy_dict)

        # 价格是字符串，需要转为int 才能使用
        if int(price_id) not in course_price_policy_dict.keys():
            ret.code= 1000
            ret.error="价格策略不符"

        # 3. 把商品和价格策略信息放入购物车 SHOPPING_CAR
        patten = "shop_car_%s_%s" %(USER_ID,course_id)
        print(patten)
        # 将数据存入radis 中, 这是这是键，用户的信息放在该内容中

        # 创建一个redis keys
        shop_key = redis_conn.keys(patten)

        # ge key中传入值，第一个为key 名
        redis_conn.hset(patten,'id',course_id)
        redis_conn.hset(patten,'name',course_obj.name)
        redis_conn.hset(patten,'img',course_obj.course_img)
        # 选择的价格
        redis_conn.hset(patten,'default_price_id',price_id)
        # 存放的是所有的价格策略
        redis_conn.hset(patten,'price_policy_dict',json.dumps(course_price_policy_dict))
        redis_conn.set("age","18")
        ret.code = 2000
        ret.data = "购买课程成功"

        return Response(ret.dict)

    def destroy(self,request,*args,**kwargs):
        return Response({'code': 11111})

    def update(self,request,*args,**kwargs):
        return Response({'code': 11111})