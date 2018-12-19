from django.urls import path

from .views import PropuestaAPIView,PropuestaAPIDetail,PropuestaAPIAllView

urlpatterns= [
	path('',PropuestaAPIView.as_view()),
	path('<int:pk>/',PropuestaAPIDetail.as_view()),
	path('all/',PropuestaAPIAllView.as_view()),
]
