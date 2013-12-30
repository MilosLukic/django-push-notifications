from rest_framework import serializers

from push_notifications.models import GCMDevice, APNSDevice


class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
        fields = ('name', 'device_id', 'registration_id',)


class APNSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = APNSDevice
        fields = ('name', 'device_id', 'registration_id',)