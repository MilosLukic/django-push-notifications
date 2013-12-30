from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from push_notifications.views import GCMDeviceDetail, APNSDeviceDetail

router = DefaultRouter()
router.register(r'gcm', GCMDeviceDetail)
router.register(r'apns', APNSDeviceDetail)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       )