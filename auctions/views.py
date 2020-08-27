from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max

from .models import User,AuctionListings,Comment,Bid,WatchList

#for creating new active listing
class listingForm(forms.Form):
    title=forms.CharField(label="title")
    price=forms.FloatField(label="price")
    img_url=forms.URLField(label="image Url")
    description=forms.CharField(widget=forms.Textarea())

class bidForm(forms.Form):
    value=forms.FloatField()





def index(request):
    return render(request, "auctions/index.html",{
        "activeListings":AuctionListings.objects.all()
    })



def listingItem(request,item_id):
    item=AuctionListings.objects.get(pk=item_id)
    bid_count=Bid.objects.count()
    print(f"bid_count:{bid_count}")
    try:
        watchlist=WatchList.objects.get(added_item=item)
        message="remove from watchlist"
    except WatchList.DoesNotExist:
        message="add to watchList"
    
    if Bid.objects.filter(bid_by=request.user).count()!=0:
        price=Bid.objects.get(bid_by=request.user).price
        bid_message=f"You have already bid for:{price}"
        has_bid=True
    else:
        has_bid=False
        bid_message="You have no bid yet"
    
    if request.method=="POST":
        if 'addOrRemove' in request.POST:
            if request.POST["addOrRemove"]=="add to watchList":
                watchListitem=WatchList(added_by=request.user,added_item=AuctionListings(pk=item_id))
                watchListitem.save()
                print(WatchList.objects.all())
                return render(request,"auctions/listingItem.html",{
                "details":item,
                    "comments":Comment.objects.filter(commented_on=item),
                    "message":"remove from watchlist",
                    "bid_counts":bid_count
        

                    })
            elif request.POST["addOrRemove"]=="remove from watchlist":
                WatchList.objects.filter(added_item=item).delete()
                return render(request,"auctions/listingItem.html",{
                "details":item,
                    "comments":Comment.objects.filter(commented_on=item),
                    "message":"add to watchList"
        

                    })
        if 'place_bid' in request.POST and has_bid==False:
            value=float(request.POST['price'])
            bid_message=place_Bid(item_id,value,current_user=request.user)
            return render(request,"auctions/listingItem.html",{
                "details":item,
                    "comments":Comment.objects.filter(commented_on=item),
                    "message":"add to watchList",
                    "bid_message":bid_message
        

                    })

    return render(request,"auctions/listingItem.html",{
        "details":item,
        "comments":Comment.objects.filter(commented_on=item),
        "message":message,
        "has_bid":has_bid,
        "bid_message":bid_message
       

    })

def createListing(request):
    if request.method=="POST":
        form=listingForm(request.POST)
        if form.is_valid():
            mtitle=form.cleaned_data["title"]
            mprice=form.cleaned_data["price"]
            mimg_url=form.cleaned_data["img_url"]
            mdescription=form.cleaned_data["description"]

            #creating new auction int auctionListing table
            new_listing=AuctionListings(title=mtitle,price=mprice,img_url=mimg_url,description=mdescription,user=request.user)
            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'auctions/createListing.html',{
                "forms":form
            })


    return render(request,"auctions/createListing.html",{
        "forms":listingForm()
    })



def watchList(request):
    items=WatchList.objects.filter(added_by=request.user)

    return render(request,"auctions/watchList.html",{
        "watchListItems":items
    })

def place_Bid(item_id,bid_price_value,current_user):
    
    bidding_item=AuctionListings.objects.get(pk=item_id)
    
    
    if bid_price_value>bidding_item.price:
        try:
            max_price=Bid.objects.aggregate(Max('price'))['price_max']
            if bid_price_value<max_price:
                #need to pass some message too
                return f"bid price must be greater than {max_price}"
                
                
            else:
                bid=Bid(bid_by=current_user,price=bid_price_value,bid_on=AuctionListings(pk=item_id))
                bid.save()
                return f"You have placed bid for {bid_price_value}"
                    
                    
                

        except KeyError:
            bid=Bid(bid_by=current_user,price=bid_price_value,bid_on=AuctionListings(pk=item_id))
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

def allBids(request,item_id):
    all_bids=Bid.objects.filter(bid_on=AuctionListings(pk=item_id))
    return render(request,"auctions/allBids.html",{
        "bids":all_bids
    })