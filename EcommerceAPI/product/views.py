from django.shortcuts import render, get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


# Create your views here.

class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        description = serializer.validated_data.get('description')
        if serializer.validated_data.get('description') is None:
            description = serializer.validated_data.get('name')
        serializer.save(description=description)

    def get_queryset(self):
        return Product.objects.all()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    queryset = Product.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj
