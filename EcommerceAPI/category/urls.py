from django.urls import path
from .views import CategoryList,CategoryDetail

urlpatterns = [
    path('', CategoryList.as_view()),
    path('<str:pk>', CategoryDetail.as_view())
]
