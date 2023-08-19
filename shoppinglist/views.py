from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Product, List, CustomUser, SharedList
from .serializers import ProductSerializer, ListSerializer, CustomUserSerializer, SharedListSerializer
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
import secrets

class ShareDataViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        user = request.user
        sharedLists = SharedList.objects.filter(user = user.id)
        serializer = SharedListSerializer(sharedLists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        data = request.data
        if (type(request.data) != dict):
            data = request.data.dict()
        sharedList = SharedList.objects.filter(list = data["list_id"])
        if sharedList.exists():
            return Response({"This list has been shared"}, status=status.HTTP_409_CONFLICT)
        # Generate a 32-character hexadecimal token
        access_token = secrets.token_hex(16)  
        data["access_token"] = access_token
        data["list"] = data["list_id"]
        data["user"] = request.user.id
        data["list_name"] = data["list_name"]
        # Store the data and access token in SharedList model
        serializer = SharedListSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk = None):
        try:
            data = request.data
            sharedList = SharedList.objects.get(id=data["pk"])
            sharedList.delete()
            deletion_successful = True
        except ObjectDoesNotExist:
            deletion_successful = False
        return Response({deletion_successful, data["pk"]}, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, access_token = None):
        sharedList = SharedList.objects.get(access_token=access_token)
        list = List.objects.get(id = sharedList.list.id)
        products = Product.objects.filter(list = list)
        productSerializer = ProductSerializer(products, many=True)
        listSerializer = ListSerializer(list)
        combinedData = {
            "products": productSerializer.data,
            "list": listSerializer.data
        }
        return Response(combinedData, status=status.HTTP_200_OK)

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        data = request.data
        if (type(request.data) != dict):
            data = request.data.dict()
        data["user"] = request.user.id
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk = None):
        product = Product.objects.get(id=pk)
        serializer  = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk = None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk = None):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            deletion_successful = True
        except ObjectDoesNotExist:
            deletion_successful = False
        return Response({deletion_successful, pk}, status=status.HTTP_202_ACCEPTED)

class ListViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.user.id
        user = get_object_or_404(CustomUser, id=user_id)
        lists = List.objects.filter(user=user)
        listSerializer = ListSerializer(lists, many=True)
        return Response(listSerializer.data)
    
    def create(self, request):
        data = request.data
        if (type(request.data) != dict):
            data = request.data.dict()
        data["user"] = request.user.id
        serializer = ListSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk = None):
        list = List.objects.get(id=pk)
        serializer  = ListSerializer(list)
        return Response(serializer.data)
    
    def update(self, request, pk = None):
        list = List.objects.get(id=pk)
        serializer = ListSerializer(instance=list, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk = None):
        try:
            list = List.objects.get(id=pk)
            list.delete()
            deletion_successful = True
        except ObjectDoesNotExist:
            deletion_successful = False
        return Response({deletion_successful, pk}, status=status.HTTP_202_ACCEPTED)

class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        password = data["password"]
        pwdEncrptedData = {}
        pwdEncrptedData["password"] = make_password(password)
        pwdEncrptedData["email"] = data["email"]
        serializer = CustomUserSerializer(data=pwdEncrptedData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)