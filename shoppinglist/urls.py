from django.urls import path
from .views import ProductViewSet, ListViewSet, UserViewSet, ShareDataViewSet


urlpatterns = [
    path('share', ShareDataViewSet.as_view({
        'post': 'create',
        'get': 'list',
        'delete': 'destroy'
    }), name="sharedList-create-list-destroy"),
    path('share/<str:access_token>', ShareDataViewSet.as_view({
        'get': 'retrieve',
    }), name="sharedList-retrieve"),
    path('products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='product-list-create'),
    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name="product-destroy-retrieve-update"),
    path('lists', ListViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name="list-list-create"),
    path('lists/<str:pk>', ListViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name="list-retrieve-update-destroy"),
    path('users', UserViewSet.as_view({
        'post': 'create'
    }), name="user-create"),
]