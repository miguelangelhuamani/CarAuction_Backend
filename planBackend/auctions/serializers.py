from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction, Bid
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field

# ------------------------------
# Category Serializers
# ------------------------------

class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# ------------------------------
# Auction Serializers
# ------------------------------

class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    # Añadimos los campos personalizados:
    auctioneer = serializers.CharField(source="auctioneer.username", read_only=True)
    auctioneer_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def validate_closing_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("La fecha de cierre no puede ser menor ni igual a la fecha de creación.")
        
        if value < timezone.now() + timedelta(days=15):
            raise serializers.ValidationError("La fecha de cierre debe ser al menos 15 días mayor que la fecha de creación.")
        
        return value

class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    auctioneer = serializers.CharField(source="auctioneer.username", read_only=True)
    auctioneer_id = serializers.IntegerField()

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

# ------------------------------
# Bid Serializers
# ------------------------------

class BidListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

    def validate(self, data):
        if data["auction"].closing_date <= timezone.now():
            raise serializers.ValidationError("La subasta ya está cerrada, no se puede pujar.")

        last_bid = Bid.objects.filter(auction=data["auction"]).order_by('-price').first()

        if last_bid and data['price'] <= last_bid.price:
            raise serializers.ValidationError(f"El precio de la nueva puja debe ser mayor que la puja ganadora actual ({last_bid.price}).")

        return data

class BidDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
