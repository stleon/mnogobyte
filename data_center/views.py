from rest_framework.viewsets import ModelViewSet
from data_center.models import *
from data_center.serializers import *
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

class DataCenterViewSet(ModelViewSet):
	queryset = DataCenter.objects.all()
	serializer_class = DataCenterSerializer

	@detail_route(methods=['GET'])
	def servers(self, request, pk):
		servers = DataCenter.servers(pk)
		resp = ServerSerializer(servers, many=True)
		return Response(resp.data)

class FloorViewSet(ModelViewSet):
	queryset = Floor.objects.all()
	serializer_class = FloorSerializer

class LocationViewSet(ModelViewSet):
	queryset = Location.objects.all()
	serializer_class = LocationSerializer

class LineViewSet(ModelViewSet):
	queryset = Line.objects.all()
	serializer_class = LineSerializer

class RackViewSet(ModelViewSet):
	queryset = Rack.objects.all()
	serializer_class = RackSerializer

	@list_route(methods=['GET'])
	def freeunits(self, request):
		# 3.5 Пользователь может просмотривать список стоек, имеющих свободные юниты
		# про корзины ничего не сказано
		racks = Rack.objects.filter(free_units_num__gte=1)
		resp = RackSerializer(racks, many=True)
		return Response(resp.data)

class BucketViewSet(ModelViewSet):
	queryset = Bucket.objects.all()
	serializer_class = BucketSerializer

class UnusedComponents():

	@list_route(methods=['GET'])
	def unused(self, request):
		serializer = self.get_serializer_class()
		unused_components = serializer.Meta.model.objects.filter(server=None)
		resp = serializer(unused_components, many=True)
		return Response(resp.data)

class ComponentViewSet(ModelViewSet, UnusedComponents):
	queryset = Component.objects.all()
	serializer_class = ComponentSerializer

class CpuSockViewSet(ModelViewSet):
	queryset = CpuSock.objects.all()
	serializer_class = CpuSockSerializer

class CpuViewSet(ModelViewSet, UnusedComponents):
	queryset = Cpu.objects.all()
	serializer_class = CpuSerializer

class HddSizeViewSet(ModelViewSet):
	queryset = HddSize.objects.all()
	serializer_class = HddSizeSerializer

class HddConnectionViewSet(ModelViewSet):
	queryset = HddConnection.objects.all()
	serializer_class = HddConnectionSerializer

class HddViewSet(ModelViewSet, UnusedComponents):
	queryset = Hdd.objects.all()
	serializer_class = HddSerializer

class RamStandartViewSet(ModelViewSet):
	queryset = RamStandart.objects.all()
	serializer_class = RamStandartSerializer

class RamViewSet(ModelViewSet, UnusedComponents):
	queryset = Ram.objects.all()
	serializer_class = RamSerializer

class RaidViewSet(ModelViewSet, UnusedComponents):
	queryset = Raid.objects.all()
	serializer_class = RaidSerializer

class NetViewSet(ModelViewSet, UnusedComponents):
	queryset = Net.objects.all()
	serializer_class = NetSerializer

class ServerTypeViewSet(ModelViewSet):
	queryset = ServerType.objects.all()
	serializer_class = ServerTypeSerializer

class ServerViewSet(ModelViewSet):
	queryset = Server.objects.all()
	serializer_class = ServerSerializer

