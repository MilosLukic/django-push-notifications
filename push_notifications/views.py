from rest_framework import viewsets, permissions

from push_notifications.models import GCMDevice, APNSDevice
from push_notifications.serializers import GCMDeviceSerializer, APNSDeviceSerializer


class GCMDeviceDetail(viewsets.ModelViewSet):
    serializer_class = GCMDeviceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return GCMDevice.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user


class APNSDeviceDetail(viewsets.ModelViewSet):
    serializer_class = APNSDeviceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return APNSDevice.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user