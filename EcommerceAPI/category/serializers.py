from rest_framework import serializers
from .models import Category
from product.serializers import ProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
