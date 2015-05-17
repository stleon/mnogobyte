from django.conf.urls import url, include
from data_center import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'data-center', views.DataCenterViewSet)
router.register(r'floor', views.FloorViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'line', views.LineViewSet)
router.register(r'rack', views.RackViewSet)
router.register(r'bucket', views.BucketViewSet)
router.register(r'components', views.ComponentViewSet)
router.register(r'cpu-sock', views.CpuSockViewSet)
router.register(r'cpu', views.CpuViewSet)
router.register(r'hdd-size', views.HddSizeViewSet)
router.register(r'hdd-connection', views.HddConnectionViewSet)
router.register(r'hdd', views.HddViewSet)
router.register(r'ram-standart', views.RamStandartViewSet)
router.register(r'ram', views.RamViewSet)
router.register(r'raid', views.RaidViewSet)
router.register(r'net', views.NetViewSet)
router.register(r'server-type', views.ServerTypeViewSet)
router.register(r'server', views.ServerViewSet)



urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]