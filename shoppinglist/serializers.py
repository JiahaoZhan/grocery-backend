from rest_framework import serializers
from .models import Product, List, CustomUser, SharedList

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class SharedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedList
        fields = '__all__'