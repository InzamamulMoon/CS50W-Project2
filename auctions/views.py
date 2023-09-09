from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


from .models import User,listings,watchlists, Comments,proffer


class Create(forms.Form):
    title=forms.CharField(label="Title", max_length=25)
    discription=forms.CharField(label="Discription", max_length=100)
    image=forms.CharField(label="Image Link")
    bid=forms.FloatField(label="Starting Bid")
    Categories=[("FA","Fashion"),
                ("TY","Toys"),
                ("EL","Electronics"),
                ("HO","Home")]
    Auction_Categories=forms.ChoiceField(widget=forms.RadioSelect,choices=Categories)

class comment(forms.Form):
    comments=forms.CharField(max_length=250,label="Comment here")

class Bid(forms.Form):
    listing_bid=forms.FloatField(label="Bid")



def index(request):
    return render(request, "auctions/index.html",{
        "listings":listings.objects.all()
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
 
def new_listings(request):
      if request.POST:
         form=Create(request.POST)
         title=request.POST['title']
         discription=request.POST['discription']
         image=request.POST['image']
         bid=request.POST['bid']
         starting_bid=request.POST['bid']
         category=request.POST['Auction_Categories']
         owner=User.objects.get(username=request.user)
         if form.is_valid():
             listings.objects.create(title=title, discription=discription,image=image,starting_bid=starting_bid,bid=bid,owner=owner,Categories=category)
             HttpResponseRedirect(reverse("index")) 
      else:     
        HttpResponseRedirect(reverse("register")) 

      return render(request, "auctions/new_listings.html",{
          "form":Create(),
          "bid":Bid()})
@login_required
def listing_page(request,listing_title):
    #need to work on the if statments here try request.get[name] for <form>
    list=listings.objects.get(title=listing_title)
    category=list.get_Categories_display()
    user_input=Comments.objects.filter(item=list)
    if not list.closing:
     if request.user.is_authenticated:
      user=User.objects.get(username=request.user)
      if list.owner==user:
         owner=True
      else:
         owner=False
      return render(request, "auctions/Listing.html",{
         "owner":owner,
         "listing":list,
         "Category":category,
         "bid":Bid(),
         "form":comment(),
         "comments": user_input})
     else:
        return render(request, "auctions/Listing.html",{
          "Category":category,
          "comments": user_input,
          "listing":list})
    else:
        highest_bid=proffer.objects.get(lisiting_bid=list.bid)
        winner=highest_bid.bidder
        watchlists.objects.filter(listing=list).delete()
        return render(request, "auctions/Listing_close.html",{
         "Category":category,
         "winner":winner,
         "listing":list,
         "comments": user_input})
    
def list_close(request,listing_title):
    list=listings.objects.get(title=listing_title) 
    list.closing=True
    list.save()
    return HttpResponseRedirect(reverse("index"))
    
 
def add_watch_list(request,listing_title):
    user=User.objects.get(username=request.user)
    list=listings.objects.get(title=listing_title)
    for val in watchlists.objects.filter(user=user):
                for item in val.listing.all():
                 if list==item:
                    return render(request,"auctions/error.html")
    if User.is_authenticated:
               person=watchlists.objects.create(user=user)
               person.save()
               person.listing.add(list)
               person.save()
               return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def remove_watch_list(request,listing_title):
    list=listings.objects.get(title=listing_title)
    if User.is_authenticated:
           watchlists.objects.filter(listing=list).delete()
           return HttpResponseRedirect(reverse("index"))
         
def watchlist_page(request):
         username=User.objects.get(username=request.user)
         person=watchlists.objects.filter(user=username)
         array=[]
         for val in person.all():
             for item in val.listing.all():
              array.append(item)
             
         #thing=watchlists.objects.filter(user=user)
         return render(request,"auctions/watchlist.html",{
            "listing":array
        })

def comments(request,listing_title):
    if request.method=="POST":
        list=listings.objects.get(title=listing_title)
        user=User.objects.get(username=request.user)
        form=comment(request.POST)
        text=request.POST["comments"]
        if form.is_valid:
           #Comments.comments=text
           #Comments.save()
           row=Comments.objects.create(comments=text,item=list,commenters=user)
           row.save() 
           #user_input=Comments.objects.filter(item=list)
           return HttpResponseRedirect(reverse("index"))
           #return render(request, "auctions/Listing.html",{"comments":user_input})

def bid(request,listing_title):
    #Create a starting_bid field for the listing model with the bid field present for the if conditon 
    if request.method=="POST":
        list=listings.objects.get(title=listing_title)
        data=list.starting_bid
        bidding=float(request.POST["listing_bid"])
        if bidding>=data or bidding>list.bid:
            list.bid=bidding
            list.save()
            user=User.objects.get(username=request.user)
            form=Bid(request.POST)
            if form.is_valid:
             new_bid_price=proffer.objects.create(lisiting_bid=bidding,treasure=list, bidder=user)
             new_bid_price.save()
        else:
            return render(request,"auctions/error.html")
            #row=proffer(listing_bid=bid, treasure=list, bidders=user)
            #row.save()
    return HttpResponseRedirect(reverse("index"))

def categories(request):
    items=listings.Auction_Categories
    key=[]
    value=[]
    for k,v in items:
        key.append(k)
        value.append(v)
    array=zip(key,value)
    return render(request, "auctions/Categories.html",{"array":array}
    )
def category_page(request,category):
        if request.method=="GET":
         items=listings.objects.filter(Categories=category)
         return render(request,"auctions/category_page.html",{"listings":items})