import json

from django.shortcuts import render, get_object_or_404
from .serializers import CartSerializer, CartItemSerializer, AddCartSerializer
from .models import Cart, CartItems
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from cache.decoding import redis_client, UUIDEncoder
from django.conf import settings


# Create your views here.

class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)
    redis_client.delete('cart_list')

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        # Check if the queryset is cached in Redis
        cache_key = 'cart_list'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            # If cached data is available, return it
            cached_data_dict = json.loads(cached_data)
            return Cart.objects.filter(id__in=cached_data_dict['ids']).order_by(*cached_data_dict['order_by'])

        # If cached data is not available, retrieve it from the database and cache it
        queryset = Cart.objects.all()
        # Serialize the queryset to JSON and cache it in Redis
        cached_data_dict = {'ids': list(queryset.values_list('id', flat=True)), 'order_by': queryset.query.order_by}
        redis_client.set(cache_key, json.dumps(cached_data_dict, cls=UUIDEncoder), settings.REDIS_CACHE_TTL)
        return queryset


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

    permission_classes = (permissions.IsAuthenticated,)
    redis_client.delete('cart_item')

    def get_queryset(self):
        # Check if the queryset is cached in Redis
        cache_key = 'cart_item'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            # If cached data is available, return it
            cached_data_dict = json.loads(cached_data)
            return CartItems.objects.filter(id__in=cached_data_dict['ids']).order_by(*cached_data_dict['order_by'])

        # If cached data is not available, retrieve it from the database and cache it
        queryset = CartItems.objects.all()
        # Serialize the queryset to JSON and cache it in Redis
        cached_data_dict = {'ids': list(queryset.values_list('id', flat=True)), 'order_by': queryset.query.order_by}
        redis_client.set(cache_key, json.dumps(cached_data_dict, cls=UUIDEncoder), settings.REDIS_CACHE_TTL)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["pk"]}
