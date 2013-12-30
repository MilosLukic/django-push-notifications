from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from push_notifications.views import GCMDeviceDetail, APNSDeviceDetail

router = DefaultRouter()
router.register(r'gcm', GCMDeviceDetail, base_name='gcm')
router.register(r'apns', APNSDeviceDetail, base_name='apns')

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       )