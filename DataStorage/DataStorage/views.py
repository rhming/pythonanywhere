from django.http import HttpRequest

# Create your views here.
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import viewsets
from DataStorage.models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ["key", "value", "createtime", "updatetime"]

    def update_or_create(self):
        model = self.Meta.model
        instance, _ = model.objects.update_or_create(
            key=self.validated_data['key'],
            defaults=self.validated_data
        )
        return instance.to_dict()

    def get(self):
        model = self.Meta.model
        try:
            instance = model.objects.get(key=self.validated_data['key'])
        except model.DoesNotExist:
            instance = None
        return instance.to_dict() if isinstance(instance, model) else instance


class DataManagerView(viewsets.ModelViewSet):
    serializer_class = DataSerializer
    authentication_classes = []
    permission_classes = []
    valid = False
    result = None
    extra = None
    def list(self, request: HttpRequest, *args, **kwargs):
        try:
            data = request.GET
            data_serializer = self.get_serializer(data=data)
            self.valid = data_serializer.is_valid(raise_exception=True)
            self.result = data_serializer.get()
            self.valid = bool(self.result and self.valid)
        except Exception as e:
            self.extra = e.args
        return Response({
            'msg': self.valid,
            'data': self.result,
            'extra': self.extra
        })
    def create(self, request: HttpRequest, *args, **kwargs):
        try:
            data = request.POST or request.data
            data_serializer = self.get_serializer(data=data)
            self.valid = data_serializer.is_valid(raise_exception=True)
            self.result = data_serializer.update_or_create()
        except Exception as e:
            self.extra = e.args
        return Response({
            'msg': self.valid,
            'data': self.result,
            'extra': self.extra
        })
