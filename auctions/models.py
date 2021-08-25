from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

 
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=13)
    comments = models.TextField(max_length=140, null=True, blank=True)
    bid = models.FloatField(max_length=2)
    photo = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=True)
    """ I wanted to add a watch category within this class since I couldn't finish watchlist in views, 
    but encounted errors within the admin page and stopped due to time restraints.
    # watch = models.BooleanField(default=False)
    """

    def __str__(self):
        return f"{self.title}: {self.description}, {self.bid}"


class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField(max_length=7)

    def __str__(self):
        return f"Enter your bid for {self.listing}: {self.bid}"


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
    

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    user = models.CharField(max_length=64)
    comment = models.TextField(max_length=140)

    def __str__(self):
        return f"{self.comment}"

    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watchlist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"
    