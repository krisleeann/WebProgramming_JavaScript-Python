from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bidding/<int:listing_id>", views.bidding, name="bidding"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:categories>", views.categories, name="categories"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
]
