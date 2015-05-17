from data_center.models import *
from rest_framework.serializers import ModelSerializer


class DataCenterSerializer(ModelSerializer):
	class Meta:
		model = DataCenter

class FloorSerializer(ModelSerializer):
	class Meta:
		model = Floor

class LocationSerializer(ModelSerializer):
	class Meta:
		model = Location

class LineSerializer(ModelSerializer):
	class Meta:
		model = Line

class RackSerializer(ModelSerializer):
	class Meta:
		model = Rack

class BucketSerializer(ModelSerializer):
	class Meta:
		model = Bucket

class ComponentSerializer(ModelSerializer):
	class Meta:
		model = Component

class CpuSockSerializer(ModelSerializer):
	class Meta:
		model = CpuSock

class CpuSerializer(ModelSerializer):
	class Meta:
		model = Cpu

class HddSizeSerializer(ModelSerializer):
	class Meta:
		model = HddSize

class HddConnectionSerializer(ModelSerializer):
	class Meta:
		model = HddConnection

class HddSerializer(ModelSerializer):
	class Meta:
		model = Hdd

class RamStandartSerializer(ModelSerializer):
	class Meta:
		model = RamStandart

class RamSerializer(ModelSerializer):
	class Meta:
		model = Ram

class RaidSerializer(ModelSerializer):
	class Meta:
		model = Raid

class NetSerializer(ModelSerializer):
	class Meta:
		model = Net
		
class ServerTypeSerializer(ModelSerializer):
	class Meta:
		model = ServerType

class ServerSerializer(ModelSerializer):
	components = ComponentSerializer(many=True, read_only=True)
	class Meta:
		model = Server



