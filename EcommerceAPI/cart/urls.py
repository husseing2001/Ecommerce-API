from django.urls import path
from .views import CartList, CartDetail, CartItemsList

urlpatterns = [
    path('', CartList.as_view()),
    path('<str:pk>', CartDetail.as_view()),
    path('items/<str:pk>', CartItemsList.as_view()),
]
