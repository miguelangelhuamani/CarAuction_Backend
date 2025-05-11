from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction, Bid, Rating, Comment
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

    # Añadir que se guarda el nombre de la categoría
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    # Añadimos los campos personalizados:
    auctioneer = serializers.CharField(source="auctioneer.username", read_only=True)

    # Aquí añadimos el campo asociado al Rating
    avg_rating = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    @extend_schema_field(serializers.DecimalField(max_digits=3, decimal_places=2))
    def get_avg_rating(self, obj):
        ratings = obj.ratings.all()

        avg = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0
        return avg
    
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
    auctioneer_id = serializers.IntegerField(read_only=True)
    
    # Aquí añadimos el campo asociado al Rating
    avg_rating = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    @extend_schema_field(serializers.DecimalField(max_digits=3, decimal_places=2))
    def get_avg_rating(self, obj):
        ratings = obj.ratings.all()

        avg = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0
        return avg
    
    def validate(self, data):
        # Validación de la fecha de cierre
        if data['closing_date'] <= data['creation_date']:
            raise serializers.ValidationError("La fecha de cierre no puede ser menor ni igual a la fecha de creación.")
        
        if data['closing_date'] < data['creation_date'] + timedelta(days=15):
            raise serializers.ValidationError("La fecha de cierre debe ser al menos 15 días mayor que la fecha de creación.")
        
        return data


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

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['auction', 'rater']
    


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user', 'user_id', 'auction']
        read_only_fields = ['user', 'created_at', 'updated_at', 'auction']
