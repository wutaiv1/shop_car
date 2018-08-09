
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CorsMiddleware(MiddlewareMixin):

    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        if request.method == "OPTIONS":
            # 设置响应头
            response["Access-Control-Allow-Methods"] = "PUT,DELETE"
            response["Access-Control-Allow-Headers"] = "Content-Type,xxxxx"
            # 在全局进行配置
            # response["Access-Control-Allow-Methods"] = settings.CORS_METHODS
            # response["Access-Control-Allow-Headers"] = settings.CORS_HEADERS
        return response