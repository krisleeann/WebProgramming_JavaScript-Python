from django.contrib import admin
from .models import User, Bidding, Comment, Listing, Watchlist, Category

# Register your models here.

# username and password: superuser
# class SuperUser(admin.ModelAdmin):
#     # superuser admin should be able to alter: listings, comments, and bids
#     view = 
#     edit = 
#     add = 
#     delete = 

admin.site.register(User)
admin.site.register(Bidding)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)