from django.urls import path
from .views import (CategoryListCreate, CategoryRetrieveUpdateDestroy, 
                    AuctionListCreate, AuctionRetrieveUpdateDestroy, BidListCreate, 
                    BidRetrieveUpdateDestroy, UserAuctionListView, UserBidListView,
                    RatingListCreate, RatingRetrieveUpdateDestroy, RatingUserAuctionView,
                    CommentListCreate, CommentRetrieveUpdateDestroy
                    )


app_name="auctions"
# El pk es la PRIMARY KEY

urlpatterns = [
    #Auctions URLs
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),



    #Categories URLs
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),

    # obtener una determinada categoría 
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),

    #Bid URLs
    path('<int:auction_id>/bids/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bids/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),

    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path('bids/users/', UserBidListView.as_view(), name='bids-from-users'),

    #Rating URLs
    path('<int:auction_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('<int:auction_id>/ratings/<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-detail'),
    path('<int:auction_id>/my-rating/', RatingUserAuctionView.as_view(), name='user-auction-rating'),


    path('<int:auction_id>/comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroy.as_view(), name='comment-detail'),
]

