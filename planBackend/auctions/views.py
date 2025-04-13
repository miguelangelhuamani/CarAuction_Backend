from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidListCreateSerializer, BidDetailSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

#PERMISOS
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]  # Solo admin puede crear/modificar categorías

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminUser]  # Solo admin puede editar/eliminar categorías

class AuctionListCreate(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Cualquier usuario autenticado puede crear subastas

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    permission_classes = [IsOwnerOrAdmin]  # Solo dueño o admin puede modificar/eliminar

class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Cualquier usuario autenticado puede pujar

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction__id=auction_id)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidDetailSerializer
    permission_classes = [IsOwnerOrAdmin]  # Solo dueño de la puja o admin puede modificar/eliminar

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction__id=auction_id)

class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]  # Correcto - solo usuarios autenticados

    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)
    
