from django.urls import path
#try listing.id or something for the urls

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listings", views.new_listings, name="new_listing"),
    path("Auction/<str:listing_title>",views.listing_page, name="listing"),
    path("Bid/<str:listing_title>", views.bid, name="bid"),
    path("Comments/<str:listing_title>", views.comments, name="comments"),
    path("watchlist_option<str:listing_title>", views.add_watch_list, name="options"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    path("item_categories", views.categories, name="Categories"),
    path("category<str:category>", views.category_page, name="category_page"),
    path("remove_watchlist_options<str:listing_title>", views.remove_watch_list, name="remove_option"),
    path("Auction_close/<str:listing_title>", views.list_close, name="close")
    
]
