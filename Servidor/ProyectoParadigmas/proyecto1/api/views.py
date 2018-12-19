from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from principal.models import Propuesta
from .serializers import PropuestaSerializer

class PropuestaAPIView(generics.ListCreateAPIView):
	queryset=Propuesta.objects.all()
	serializer_class=PropuestaSerializer
	
class PropuestaAPIDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=Propuesta.objects.all()
	serializer_class=PropuestaSerializer
	
class PropuestaAPIAllView(generics.ListAPIView):
	queryset=Propuesta.objects.all()
	serializer_class=PropuestaSerializer