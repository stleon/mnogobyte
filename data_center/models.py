from django.db import models
from django.core.exceptions import ValidationError

class CommonInfo(models.Model):
	name = models.CharField('Название', max_length=128,)

	class Meta:
		abstract = True

	def __str__(self):
		return self.name


class DataCenter(CommonInfo):
	adress = models.CharField('Адрес', max_length=128,)

	def servers(self):
		servers_in_rack = Server.objects.filter(rack__line__location__floor__data_center=self)
		servers_in_bucket = Server.objects.filter(bucket__rack__line__location__floor__data_center=self)
		return servers_in_rack | servers_in_bucket


class Floor(CommonInfo):
	data_center = models.ForeignKey(DataCenter,)


class Location(CommonInfo):
	floor = models.ForeignKey(Floor,)


class Line(CommonInfo):
	location = models.ForeignKey(Location,)


class UnitsBase(models.Model):
	# чтобы каждый раз не высчитывать для каждой стойки в цикле, сразу будем сохранять
	free_units_num = models.PositiveIntegerField('Количество свободных юнитов')
	units_num = models.PositiveIntegerField('Количество юнитов')

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):

		if self.free_units_num > self.units_num:
			raise Exception('impossible configuration: num of free units > num of units')

		super(UnitsBase, self).save(*args, **kwargs)


class Rack(CommonInfo, UnitsBase):
	line = models.ForeignKey(Line,)


def rack_minus_free_units(obj):
	'''можно было сделать и статическим методом CommonInfo'''
	if obj.rack.free_units_num >= obj.units_height:
		obj.rack.free_units_num -= obj.units_height
		obj.rack.save()
	else:
		raise Exception('no aviable units')


class Bucket(CommonInfo, UnitsBase):
	rack = models.ForeignKey(Rack, blank=True, null=True,)
	units_height = models.PositiveIntegerField('Высота в юнитах')

	def save(self, not_server=True, *args, **kwargs):

		if self.rack and not_server:
			# если по размерам все подходит, вычитаем из свободных и сейв
			rack_minus_free_units(self)			

		super(Bucket, self).save(*args, **kwargs)

class CpuSock(CommonInfo):
	sock = models.CharField('Сокет', max_length=8,)


class HddSize(CommonInfo):
	standart_size = models.CharField('Типоразмер', max_length=128,)


class HddConnection(CommonInfo):
	connection_standart = models.CharField('Стандарт подключения', max_length=128,)


class RamStandart(CommonInfo):
	standart = models.CharField('Стандарт', max_length=128,)


class ServerType(CommonInfo):
	sock = models.ForeignKey(CpuSock,)
	hdd_standart_size = models.ManyToManyField(HddSize,)
	hdd_connection_standart = models.ForeignKey(HddConnection,)
	ram_standart = models.ForeignKey(RamStandart,)
	cpu_num = models.PositiveIntegerField('Количество ядер', default=2)
	hdd_num_slots = models.PositiveIntegerField('Количество слотов HDD', default=4)
	ram_num_slots = models.PositiveIntegerField('Количество слотов RAM', default=8)


class Server(CommonInfo):
	server_type = models.ForeignKey(ServerType,)
	rack = models.ForeignKey(Rack, related_name='in_rack', blank=True, null=True,)
	bucket = models.ForeignKey(Bucket, related_name='in_bucket', blank=True, null=True,)
	units_height = models.PositiveIntegerField('Высота в юнитах')

	def save(self, *args, **kwargs):
		if self.bucket and self.rack:
			raise Exception('impossible configuration')
		
		# Про сокращение свободных мест ничего не говорилось
		# код дублируется, dry не соблюдается
		elif self.bucket:
			if self.bucket.free_units_num >= self.units_height:
				self.bucket.free_units_num -= self.units_height
				self.bucket.save(not_server=False)
			else:
				raise Exception('no aviable units')

		elif self.rack:
			rack_minus_free_units(self)

		super(Server, self).save(*args, **kwargs)


class Component(CommonInfo):
	server = models.ForeignKey(Server, blank=True, null=True, related_name='components',)
	manufacturer = models.CharField('Производитель', max_length=128,)
	c_model = models.CharField('Модель', max_length=128,)
	serial_number = models.CharField('Серийный номер', unique=True, max_length=128,)

	def save(self, *args, **kwargs):
		# такую же проверку можно сделать при сохр сервера, атрибуты поменять
		if self.server:
			if hasattr(self, 'sock'):
				if self.sock != self.server.server_type.sock:
					raise Exception('did not match sockets')
			if hasattr(self, 'hdd_connection_standart'):
				if self.hdd_connection_standart != self.server.server_type.hdd_connection_standart:
					raise Exception('did not match hdd_connection_standart')
			if hasattr(self, 'ram_standart'):
				if self.ram_standart != self.server.server_type.ram_standart:
					raise Exception('did not match ram_standart')

		super(Component, self).save(*args, **kwargs)

class Cpu(Component):
	sock = models.ForeignKey(CpuSock,)

class Hdd(Component):
	hdd_types = (
		('0', 'HDD'),
		('1', 'SDD'),
		('2', 'Hybdrid'),
	)
	hdd_standart_size = models.ForeignKey(HddSize,)
	hdd_connection_standart = models.ForeignKey(HddConnection,)
	volume = models.PositiveIntegerField('Объем', default=1024)
	hdd_type = models.CharField('Тип', max_length=1, choices=hdd_types, default=0)


class Ram(Component):
	ram_standart = models.ForeignKey(RamStandart,)
	volume = models.PositiveIntegerField('Объем', default=1024)

class Raid(Component):
	connection_type = models.CharField('Тип подключения', max_length=128,)

class Net(Component):
	connection_type = models.CharField('Тип подключения', max_length=128,)
