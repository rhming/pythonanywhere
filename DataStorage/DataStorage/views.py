from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.views import View


# Create your views here.
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import viewsets
from DataStorage.models import Data


# def delete(key):
#     try:
#         Data.objects.get(key=key).delete()
#     except Data.DoesNotExist:
#         pass


def update_or_create(key, value):
    try:
        if not (key and value):
            raise Exception('传输数据错误')
        Data.objects.update_or_create(key=key, defaults={"key": key, "value": value})
        return {
            'msg': 'success',
            'code': 200
        }
    except Exception as e:
        return {
            'msg': str(e),
            'code': -1
        }


def query(key):
    try:
        data = Data.objects.get(key=key)
        return {
            "msg": "success",
            "data": {
                key: data.value,
                "时间": data.createtime
            },
            "code": 200
        }
    except Data.DoesNotExist:
        return {
            "msg": "参数key错误",
            "code": -1
        }


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ["key", "value", "createtime"]


class TestView(viewsets.GenericViewSet):

    renderer_classes = [BrowsableAPIRenderer, JSONRenderer, ]
    serializer_class = TestSerializer

    def select(self, request: HttpRequest, *args, **kwargs):
        data = request.GET
        key = data.get('key', '')
        result = query(key)
        return Response(result)

    def insert(self, request: HttpRequest, *args, **kwargs):
        data = request.POST or request.data
        key = data.get('key',  None)
        value = data.get('value', None)
        result = update_or_create(key, value)
        return Response(result)


'''
class DataManagerView(View):

    def get(self, request: HttpRequest, *args, **kwargs):
        data = request.GET
        key = data.get('key', '')
        result = query(key)
        return JsonResponse(result)

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST
        key = data.get('key',  None)
        value = data.get('value', None)
        result = update_or_create(key, value)
        return JsonResponse(result)
'''

