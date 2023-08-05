# -*- coding:utf-8 -*-
from django_szuprefix.api.mixins import BatchActionMixin

from .apps import Config

from . import models, mixins, serializers, permissions

from rest_framework import viewsets, decorators, response
from django_szuprefix.api.helper import register
from django_szuprefix.api.permissions import DjangoModelPermissionsWithView

__author__ = 'denishuang'


class WorkerViewSet(mixins.PartyMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Worker.objects.all()
    serializer_class = serializers.WorkerSerializer
    permission_classes = [DjangoModelPermissionsWithView]
    filter_fields = {
        'number': ['exact', 'in']
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WorkerListSerializer
        return super(WorkerViewSet, self).get_serializer_class()

    @decorators.list_route(['get'], permission_classes=[permissions.IsSaasWorker])
    def current(self, request):
        serializer = serializers.CurrentWorkerSerializer(self.worker, context={'request': request})
        return response.Response(serializer.data)


    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)


register(Config.label, 'worker', WorkerViewSet)
