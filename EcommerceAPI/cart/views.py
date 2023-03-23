from django.shortcuts import render, get_object_or_404
from .serializers import CartSerializer, CartItemSerializer, AddCartSerializer
from .models import Cart, CartItems
from rest_framework import generics, permissions


# Create your views here.

class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = 'pk'
    queryset = Cart.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj


class CartItemsList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItems.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartSerializer
        return CartItemSerializer

    def get_serializer_context(self):
         return {"cart_id": self.kwargs["pk"]}
