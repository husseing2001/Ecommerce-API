from django.shortcuts import render, get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
import redis
import json
from cache.decoding import redis_client,UUIDEncoder
from django.conf import settings

# Create your views here.


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    redis_client.delete('product_list')

    def perform_create(self, serializer):
        description = serializer.validated_data.get('description')
        if serializer.validated_data.get('description') is None:
            description = serializer.validated_data.get('name')
        serializer.save(description=description)

    def get_queryset(self):
        # Check if the queryset is cached in Redis
        cache_key = 'product_list'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            # If cached data is available, return it
            cached_data_dict = json.loads(cached_data)
            return Product.objects.filter(id__in=cached_data_dict['ids']).order_by(*cached_data_dict['order_by'])

        # If cached data is not available, retrieve it from the database and cache it
        queryset = Product.objects.all()
        # Serialize the queryset to JSON and cache it in Redis
        cached_data_dict = {'ids': list(queryset.values_list('id', flat=True)), 'order_by': queryset.query.order_by}
        redis_client.set(cache_key, json.dumps(cached_data_dict, cls=UUIDEncoder), settings.REDIS_CACHE_TTL)
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    queryset = Product.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj
