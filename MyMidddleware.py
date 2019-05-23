from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class Md1(MiddlewareMixin):
    def process_request(self,request):
        print('Md1请求')
        # return HttpResponse('中断')

    def process_response(self,request,response):
        print('Md1响应')
        return response


class Md2(MiddlewareMixin):
    def process_request(self, request):
        print('Md2请求')
        return HttpResponse('中断')

    def process_response(self, request, response):
        print('Md2响应')
        return response