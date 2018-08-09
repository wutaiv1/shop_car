import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination

from api import models
from api.serializers.course import CourseSerializer,CourseModelSerializer,CoursePriceSerializer
from api.utils.response import BaseResponse


class CoursesView(APIView):

    def get(self,request,*args,**kwargs):
        #response = {'code':1000,'data':None,'error':None}
        ret = BaseResponse()
        try:
            # 从数据库获取数据
            queryset = models.Course.objects.all()
            print(queryset)

            # 分页
            page = PageNumberPagination()
            course_list = page.paginate_queryset(queryset,request,self)

            print(course_list)
            # 分页之后的结果执行序列化
            ser = CourseSerializer(instance=course_list,many=True)

            print(ser.data)
            # response["data"] = ser.data
            ret.data = ser.data
            print("aaaaa",ret.dict)
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'


        return Response(ret.dict)


class CoursesPrice(APIView):

    def get(self,request,*args,**kwargs):
        #response = {'code':1000,'data':None,'error':None}
        ret = BaseResponse()
        try:
            # 从数据库获取数据
            queryset = models.Course.objects.all()
            print(queryset)


            # 分页之后的结果执行序列化
            ser = CoursePriceSerializer(instance=queryset,many=True)

            ret.data = ser.data
            print("aaaaa",ret.dict)
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'


        return Response(ret.dict)