from wang.lib.proof import *
from rest_framework import serializers
from principal.models import Propuesta
from wang.src.wang import *
import json
class PropuestaSerializer(serializers.ModelSerializer):
	class Meta:
		model=Propuesta
		fields=('id','propuesta','respuesta')
		
	def create(self,data):
		print(f">>>Create {data}")
		prop= data['propuesta']
		# print(f">>>propuesta {prop}")
		result=evaluacion(prop)
		rstree=recorrerArbol(result)
		data['respuesta']=rstree.__str__()
		return super().create(data)
