import json

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Category
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer
from rest_framework import generics
from cache.decoding import redis_client, UUIDEncoder


# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    redis_client.delete('category_list')

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        # Check if the queryset is cached in Redis
        cache_key = 'category_list'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            # If cached data is available, return it
            cached_data_dict = json.loads(cached_data)
            return Category.objects.filter(id__in=cached_data_dict['ids']).order_by(*cached_data_dict['order_by'])

        # If cached data is not available, retrieve it from the database and cache it
        queryset = Category.objects.all()
        # Serialize the queryset to JSON and cache it in Redis
        cached_data_dict = {'ids': list(queryset.values_list('id', flat=True)), 'order_by': queryset.query.order_by}
        redis_client.set(cache_key, json.dumps(cached_data_dict, cls=UUIDEncoder), settings.REDIS_CACHE_TTL)
        return queryset


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    queryset = Category.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj
