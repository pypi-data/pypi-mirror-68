from django.db import models
from ..utils.constants import short_name_len , value_len
from .experi import Experiment

class SingleValue(models.Model):
	'''某个变量的某条时间线上的一个值
	'''
	value = models.CharField(max_length = value_len)
	time_stamp = models.IntegerField()
	track = models.ForeignKey("VariableTrack" , on_delete = models.CASCADE , related_name = "values")

class VariableTrack(models.Model):
	'''某个变量的一条时间线
	'''
	name = models.CharField(max_length = short_name_len)
	variable = models.ForeignKey("Variable" , on_delete = models.CASCADE , related_name = "tracks")

	def __str__(self):
		return self.name

class Variable(models.Model):
	name = models.CharField(max_length = short_name_len)
	expe = models.ForeignKey(Experiment , on_delete = models.CASCADE , related_name = "variables")

	def __str__(self):
		return self.name

__all__ = [
	"SingleValue" , 
	"VariableTrack" , 
	"Variable" , 
]