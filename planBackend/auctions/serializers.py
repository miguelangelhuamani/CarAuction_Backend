<<<<<<< HEAD
from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction, Bid
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field

# Category Serializers
class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Auction Serializers
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
        # Validación de la fecha de cierre
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


#Bid Serializers
class BidListCreateSerializer(serializers.ModelSerializer):
    auction_title = serializers.CharField(source="auction.title", read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'amount', 'creation_date', 'auction_title']

    def validate(self, data):
        request = self.context.get("request")
        auction_id = self.context["view"].kwargs.get("auction_id")

        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise serializers.ValidationError("Subasta no encontrada.")

        # Validación de fecha de cierre
        if auction.closing_date <= timezone.now():
            raise serializers.ValidationError("La subasta ya está cerrada, no se puede pujar.")

        # Validación de monto
        last_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
        if last_bid and data["amount"] <= last_bid.amount:
            raise serializers.ValidationError(
                f"Tu puja debe ser mayor a la actual: {last_bid.amount}"
            )

        return data

class BidDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
=======
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
>>>>>>> main
