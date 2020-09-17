from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListings, Comment, Bid, WatchList
from django.contrib.auth.models import AnonymousUser

# for creating new active listing


class listingForm(forms.Form):
    title = forms.CharField(label="title")
    price = forms.FloatField(label="price")
    img_url = forms.URLField(label="image Url")
    description = forms.CharField(widget=forms.Textarea())


class bidForm(forms.Form):
    value = forms.FloatField()


def index(request):
    return render(request, "auctions/index.html", {
        "activeListings": AuctionListings.objects.all()
    })


def listingItem(request, item_id):
    listing_owner = False
    message=""
    item = AuctionListings.objects.get(pk=item_id)
    bid_count = Bid.objects.count()
    print(f"bid_count:{bid_count}")
    if request.user == item.user:
        listing_owner = True
    try:
        watchlist = WatchList.objects.get(added_item=item)
        message = "remove from watchlist"
    except WatchList.DoesNotExist:
        message = "add to watchList"
    
    print(request.user)
    #need to show data also during logged out time--------------------------------------------------
    
   
    if request.user.is_authenticated:
        if Bid.objects.filter(bid_by=request.user, bid_on=AuctionListings(pk=item_id)).count() != 0:
            price = Bid.objects.get(bid_by=request.user,bid_on=item).price
            bid_message = f"You have already bid for:{price}"
            has_bid = True
        else:
            has_bid = False
            bid_message = "You have no bid yet"





    
    if request.method == "POST":
        if 'addOrRemove' in request.POST:
            if request.POST["addOrRemove"] == "add to watchList":
                watchListitem = WatchList(
                    added_by=request.user, added_item=AuctionListings(pk=item_id))
                watchListitem.save()
                print(WatchList.objects.all())
                return render(request, "auctions/listingItem.html", {
                    "details": item,
                    "comments": Comment.objects.filter(commented_on=item),
                    "message": "remove from watchlist",
                    "bid_counts": bid_count,
                    "creator": listing_owner


                })
            elif request.POST["addOrRemove"] == "remove from watchlist":
                WatchList.objects.filter(added_item=item).delete()
                return render(request, "auctions/listingItem.html", {
                    "details": item,
                    "comments": Comment.objects.filter(commented_on=item),
                    "message": "add to watchList"


                })
        if 'place_bid' in request.POST and has_bid == False:
            value = float(request.POST['price'])
            bid_message = place_Bid(item_id, value, current_user=request.user)
            return render(request, "auctions/listingItem.html", {
                "details": item,
                "comments": Comment.objects.filter(commented_on=item),
                "message": "add to watchList",
                "bid_message": bid_message,
                "creator": listing_owner


            })
        if 'cancel_bid' in request.POST:
            item.bid_active = False
            item.save()

            print(f"item_active:{item.bid_active}")
            return HttpResponseRedirect(request.path_info)

    return render(request, "auctions/listingItem.html", {
        "details": item,
        "comments": Comment.objects.filter(commented_on=item),
        "message": message,
       
        
        "creator": listing_owner


    })


def createListing(request):
    if request.method == "POST":
        form = listingForm(request.POST)
        if form.is_valid():
            mtitle = form.cleaned_data["title"]
            mprice = form.cleaned_data["price"]
            mimg_url = form.cleaned_data["img_url"]
            mdescription = form.cleaned_data["description"]

            # creating new auction int auctionListing table
            new_listing = AuctionListings(
                title=mtitle, price=mprice, img_url=mimg_url, description=mdescription, user=request.user)
            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/createListing.html', {
                "forms": form
            })

    return render(request, "auctions/createListing.html", {
        "forms": listingForm()
    })


def watchList(request):
    items = WatchList.objects.filter(added_by=request.user)

    return render(request, "auctions/watchList.html", {
        "watchListItems": items
    })


def place_Bid(item_id, bid_price_value, current_user):

    bidding_item = AuctionListings.objects.get(pk=item_id)

    if bid_price_value > bidding_item.price:
        try:
            max_price = Bid.objects.filter(bid_on=bidding_item).aggregate(Max('price'))['price__max']
            #if no bids max price returns none
            if max_price==None:
                max_price=0.0
            if  bid_price_value < max_price:
                # need to pass some message too
                return f"bid price must be greater than {max_price}"

            else:
                bid = Bid(bid_by=current_user, price=bid_price_value,
                          bid_on=AuctionListings(pk=item_id))
                bid.save()
                return f"You have placed bid for {bid_price_value}"

        except KeyError:
            bid = Bid(bid_by=current_user, price=bid_price_value,
                      bid_on=AuctionListings(pk=item_id))
            bid.save()
            return f"You have placed bid for {bid_price_value}"
    else:
        return "bid price must be greater than the price of item"


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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


# need to workout on this method to display winner after bid closed-----------------------

def allBids(request, item_id):
    has_bid=False
    all_bids = Bid.objects.filter(bid_on=AuctionListings(pk=item_id))
    bid_nums=all_bids.count()
    print(bid_nums)
    if bid_nums!=0:
        has_bid=True
    item=AuctionListings.objects.get(pk=item_id)
    is_active=item.bid_active
    if has_bid:
        if not is_active:
        
            requested_user_wins = False
            maximum_price=all_bids.aggregate(Max("price"))['price__max']
            
            print(f"maxprice:{maximum_price}")
            winner = all_bids.get(price=maximum_price)
            print(winner.bid_by)
            
            if winner is not None:
                if request.user == winner.bid_by:
                    requested_user_wins = True

                return render(request, "auctions/allBids.html", {
                    "bids": all_bids,
                    "winner": winner,
                    "you_won": requested_user_wins,
                    "has_winner": True,
                    "has_bid":has_bid
                    
                    
                })
        
        

    return render(request, "auctions/allBids.html", {
        "bids": all_bids,
        "has_bid":has_bid,
        "has_winner": False
    })

def Comments(request,item_id):
    if request.method=="POST":
        item_id=int(request.POST["item_id"])
        
        cmt=request.POST["comment"]
        comment=Comment(comment=cmt,commented_by=request.user,commented_on=AuctionListings(pk=item_id))
        comment.save()
    url=reverse("listingItem",args=(item_id,))#here i was stuck for long time for not using args=(item_id,)
    return HttpResponseRedirect(url)
    #this redirect not working need to check later
