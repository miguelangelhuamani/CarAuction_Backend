from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from .models import Category, Auction, Bid, Rating, Comment
from .serializers import (CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, 
                          BidListCreateSerializer, BidDetailSerializer, RatingSerializer, CommentSerializer)
from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

#PERMISOS
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin, IsRatingOwnerOrAdmin

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Solo admin puede crear/modificar categorías

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    #permission_classes = [IsAdminUser]  # Solo admin puede editar/eliminar categorías

class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Cualquier usuario autenticado puede crear subastas

    def get_queryset(self): 
        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('search')
        category = params.get('category')
        open = params.get('open')
        order = params.get('order')

        if search and len(search) <1: # validación para comprobar que la querysearch sea de como mínimo 1 caracter
            raise ValidationError("La búsqueda debe tener al menos 1 carácter",             
                                    code=status.HTTP_400_BAD_REQUEST)


        if search:
            # Aplicar el filtro tanto a la descripción como al título
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search)) 

        if category:
            queryset = queryset.filter(category__id=category)
        
        if open:
            if open == "true":
                queryset = queryset.filter(closing_date__gt = timezone.now())
            else:
                queryset = queryset.filter(closing_date__lt = timezone.now())

        if order == "asc":
            queryset = queryset.order_by("price")

        elif order == "desc":
            queryset = queryset.order_by("-price")


        return queryset

    def perform_create(self, serializer):
        # Guardar el usuario autenticado como subastador
        serializer.save(auctioneer=self.request.user)

        Rating.objects.create(
            rating=1.0, # por defecto 1.0
            auction=serializer.instance,
            rater=self.request.user
        )

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    permission_classes = [IsOwnerOrAdmin]  # Solo dueño o admin puede modificar/eliminar

class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        queryset= Bid.objects.filter(auction__id=auction_id)
        return queryset
    
    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        auction = Auction.objects.get(pk=auction_id)
        serializer.save(bidder=self.request.user, auction=auction)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidDetailSerializer
    permission_classes = [IsOwnerOrAdmin]  # Solo dueño de la puja o admin puede modificar/eliminar

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction__id=auction_id)

class UserAuctionListView(APIView):
    # Listar todas las subastas asociadas a un usuario
    permission_classes = [IsAuthenticated]  # Correcto - solo usuarios autenticados

    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)

class UserBidListView(APIView):
    # Registrar las pujas de un usuario en completo
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_bids = Bid.objects.filter(bidder=request.user)
        serializer = BidListCreateSerializer(user_bids, many=True)
        return Response(serializer.data)



# Rating Views
class RatingListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        auction_id = self.kwargs['auction_id']
        ratings = Rating.objects.filter(auction__id=auction_id)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        # Validar que cada usuario valora solo una cez una subasta
        auction_id = self.kwargs['auction_id']
        auction = Auction.objects.get(pk=auction_id)

        if Rating.objects.filter(auction=auction, rater=request.user).exists():
            raise ValidationError("Ya has valorado esta subasta.")

        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rater=self.request.user, auction=auction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsRatingOwnerOrAdmin]  # Solo dueño de la valoración o admin puede modificar/eliminar

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Rating.objects.filter(auction__id=auction_id)

class RatingUserAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, auction_id):
        try:
            rating = Rating.objects.get(auction__id=auction_id, rater=request.user)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        
        except Rating.DoesNotExist:
            return Response({"detail": "No has valorado esta subasta."}, status=404)

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Comment.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        serializer.save(user=self.request.user, auction_id=auction_id)

class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    #permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Comment.objects.all()