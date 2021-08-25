from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import Category, Comment, Bidding, Listing, User, Watchlist
from .forms import NewEntryForm, NewCommentForm


# Following index, all functions are arranged alphabetically 
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


@login_required  
def bidding(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        category = listing.category()
        comments = Comment.objects.filter(listing=listing_id)
        bid = request.POST["bid"]
        updated = float(bid) 

        if listing.user == True:
            owner = True
        else:
            owner = False

        if updated < current:
            return render(request, "auctions/bidding.html", {
                "message": "New bid cannot be less than current bid. Please increase your bid and try again."
            })
        else:
            # HOW DO I SAVE USER INPUT AS A NEW BID? 
            bid = updated
            listing.save()

            return render(request, "auctions/bidding.html", {
                "user": user,
                "owner": owner,
                "listing": listing,
                "category": category,
                "comments": comments,
                "bid": bid,
                "updated": updated
            })


# Closed bidding, means highest bidder win
# html check if listing is closed AND if user viewing is user with highest bid
def bidding_closed(request, listing_id):
    pass


def categories(request):
    categories = Category.objects.all()
    category = None
    listing = None

    if request.method == "POST":
        categories = request.POST["categories"]
        listing = Listing.objects.filter(category=categories)
    
        return render(request, "auctions/categories.html", {
            "listings": listing,
            "category": Category.objects.get(id=category).category if category is not None else "",
            "categories": categories,
        })
    else:
        return render(request, "auctions/categories.html", {
            "listings": listing,
            "message": "Categories have not been created yet. Create one and try again!"
        })


@login_required
def close_listing(request, listing_id):
    listing = listing(request, listing_id)
    listing.active = False
    listing.save()

    winner = Bidding.objects.get(highest=listing.bid, listing=listing).user

    if winner: 
        return render(request, "auctions/close_listing.html", {
            "listing": listing, 
            "winner": winner,
            "message": "Congrats! You won the bidding!"
        })
    else:
        return render(request, "auctions/close_listing.html", {
            "message": "We're sorry, the listing was sold to another user."
        })

@login_required
def comment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        listing = Listing.objects.get(id=listing)

        listing.comments.add(Comments.objects.create(comment=comment, user=request.user))
        listing.save()
    return HttpResponseRedirect(request, "auction/comments.html")


# Unfinished. 'Active Listings' page does not load properly. 
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    
    if listing.user == True:
        owner = True
    else:
        owner = False

    if request.method == "POST":        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "owner": owner,
            "category": Category.objects.get(listing=listing.id),
            "comments": Comment.objects.filter(listing=listing_id),
            "comment": NewCommentForm(),
            "active": Listing.objects.filter(active=True),
        })
    else:
        return render(request, "auctions/listing.html", {
            "message": "No listings have been created yet. Try creating one now!"
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "auctions/index.html", {
                "listings": Listing.objects.filter(active=True)
            })
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create a new listing, reused code from the wiki project
# Unfinished. 'Active Listings' page does not load properly. 
@login_required
def new_listing(request):

    if request.method == "POST":
        # Accept user input and save as form 
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            category = Category.cleaned_data(id=request.POST["category"])
            photo = form.cleaned_data["photo"]

            Listing.objects.create(user=user, title=title, bid=bid, description=description, 
                category=category, photo=photo)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/new_listing.html", {
            "listing": NewEntryForm(),
            "categories": Category.objects.all() 
        })


@login_required
def watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    items = []

    if watchlist == None: 
        return render(request, "auctions/watchlist.html", {
            "message": "Any listings you add to your watchlist will appear here!",
        })
    else:
        for saved in watchlist:
            items.append(Listing.objects.filter(id=saved.listing_id))

        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist, 
            "items": items
        })


# Ran out of time and couldn't debug. 
@login_required
def watchlist_add(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    user.watchlist = False
    watchlist.save()

    return render(request, "auctions/watchlist.html", {
        "listing": listing,
        "watchlist": watchlist
    })


# Ran out of time and couldn't debug. 
@login_required
def watchlist_remove(request):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    user.watchlist = True
    watchlist.save()

    return render(request, "auctions/watchlist.html", {
        "listing": listing,
        "watchlist": watchlist
    })