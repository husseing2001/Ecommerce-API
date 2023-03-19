from rest_framework import serializers
from .models import Cart, CartItems
from product.serializers import ProductSerializer
from product.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    product = ProductSerializer(many=False)

    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItems
        fields = ['id', 'cart_id', 'product', 'quantity','sub_total']

    def total(self, cartitem):
        if cartitem.product and cartitem.product.price is not None:
            return cartitem.quantity * cartitem.product.price
        else:
            return 0


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']


class AddCartSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validated_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            return serializers.ValidationError("No product with given id")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cartitem = CartItems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
        except:
            self.instance = CartItems.objects.create(product_id=product_id, cart_id=cart_id, quantity=quantity)
        return self.instance
    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'quantity']
