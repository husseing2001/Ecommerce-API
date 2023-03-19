from django.shortcuts import render, get_object_or_404
from .models import Category
from .serializers import CategorySerializer
from rest_framework import generics


# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    queryset = Category.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj
