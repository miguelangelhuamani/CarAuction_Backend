from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidListCreateSerializer, BidDetailSerializer

from django.db.models import Q  #Para la validación de filtro

# Category Views
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


# Auction Views
class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('text', None)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        category = params.get('category', None)
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        min_price = params.get("MinPrice", None)
        max_price = params.get("MaxPrice", None)
        if min_price is not None and max_price is not None:
            queryset = queryset.filter(starting_price__gte=min_price, starting_price__lte=max_price)
        elif min_price is not None:
            queryset = queryset.filter(starting_price__gte=min_price)
        elif max_price is not None:
            queryset = queryset.filter(starting_price__lte=max_price)

        return queryset


class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


# Bid Views
class BidListCreate(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidListCreateSerializer

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidDetailSerializer