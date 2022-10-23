from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import ProductFilter
from store.pagination import DefaultPagination

from store.serializers import CartSerializer, ProductSerialzier, CollectionSerializer, ReviewSerializer
from .models import Cart, Collection, OrderItem, Product, Review


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerialzier
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can not be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(products=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection can not be deleted b/c it includes one or more products'})
        return super().destroy(request, *args, **kwargs)

    # def destory(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection can not be deleted b/c it includes one or more products'})
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('carts__product').all()
    serializer_class = CartSerializer
