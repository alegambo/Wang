from django.db import models
from jsonfield import JSONCharField
# Create your models here.
class Propuesta(models.Model):
	propuesta=models.CharField(max_length=100)
	respuesta=models.TextField(null=True)
	def __str__(self):
		return self.propuesta
