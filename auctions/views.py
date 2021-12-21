from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, Max

from .models import User,Category,AuctionListing,Comment,Bid,Watchlist

class SelectForm(forms.Form):
    select = forms.ModelChoiceField(queryset=Category.objects.all(),required=False)
    maxprice = forms.FloatField(required=False)

class BidForm(forms.Form):
    bid = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control m-1','placeholder': 'Your bid'}))

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

def index(request):

    if  request.method == 'POST':
        form = SelectForm(request.POST)

        if form.is_valid():
            selected = form.cleaned_data['select']
            maxpriced = form.cleaned_data['maxprice']
            query = QueryDict(mutable=True)
            
            if selected is None:
                query.__setitem__('select',None)
            else:
                query.__setitem__('select',selected.id)
                
            query.__setitem__('maxprice',maxpriced)
            url = reverse('filter', kwargs={'filter': query.urlencode() })
            return HttpResponseRedirect(url)
    
    

    return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":SelectForm()
    })

def search(request):
    if  request.method == 'GET':
        search_input = request.GET['search_input']
        print(search_input)

        return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all().filter(title__contains=search_input),
        "selectform":SelectForm()
        })
    


def sidebar_filter(request,filter):

    query = QueryDict(query_string=filter)

    stringCategoryId = query.get("select",'')
    stringMaxPrice = query.get("maxprice",'')

    categoryId =int(stringCategoryId) if stringCategoryId != 'None' else None 
    maxprice =float(stringMaxPrice) if stringMaxPrice != 'None' else None

    if categoryId is None:
        form = SelectForm(initial = {'maxprice':maxprice })
    else:
        form = SelectForm(initial = {'select': Category.objects.get(id=categoryId),'maxprice':maxprice })

    auctionquery=AuctionListing.getFilteredByCategoryAndPrice(categoryId,maxprice)
 
    return render(request,"auctions/index.html",{
        "auctions":auctionquery,
        "selectform":form

    })


def addToWatch(request,listing_id):
    if request.user.is_authenticated:
        user = request.user
        if not Watchlist.objects.filter(user=user,auctionlisting=AuctionListing.objects.get(id=listing_id)).exists():
            wlitem = Watchlist(user=user,auctionlisting=AuctionListing.objects.get(id=listing_id))
            wlitem.save()
            return render(request,"auctions/watchlist.html",{
                "watchlist":Watchlist.objects.all().filter(user=user)
                })
        else:
            return render(request,"auctions/watchlist.html",{
                "watchlist":Watchlist.objects.all().filter(user=user)
                })
    else:
        return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":SelectForm()
        })
            


def watchList(request):

    if request.user.is_authenticated:
        user=request.user
        return render(request,"auctions/watchlist.html",{
                "watchlist":Watchlist.objects.all().filter(user=user)
                })
    else:
        return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":SelectForm()
        })

    
    


def showListing(request,listing_id):

    if  request.method == 'POST' and request.POST.get('iscomment') != 'true':
        form = BidForm(request.POST)
        
        
        if form.is_valid():
            bid = form.cleaned_data['bid']
            if request.user.is_authenticated:
                user = request.user
                
                if bid > AuctionListing.objects.get(id=listing_id).getPrice():
                    b = Bid(user=user, auctionlisting=AuctionListing.objects.get(id=listing_id),bid=bid)
                    b.save()
            url = reverse('showListing', kwargs={'listing_id': listing_id })
            return HttpResponseRedirect(url)  
    elif request.method == 'POST' and request.POST.get('iscomment') == 'true':
        form = CommentForm(request.POST)
        if form.is_valid():
            commenttext = form.cleaned_data['comment']
            if request.user.is_authenticated:
                user = request.user
                c = Comment(user=user,auctionlisting=AuctionListing.objects.get(id=listing_id),comment=commenttext)
                c.save()
                url = reverse('showListing', kwargs={'listing_id': listing_id })
                return HttpResponseRedirect(url)


    try:
        litem=AuctionListing.objects.get(id=listing_id)
    except AuctionListing.DoesNotExist:
        litem = None


    if litem is None:
        return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":SelectForm(),
        "commentform":CommentForm(),
        "comments":Comment.objects.all().filter(auctionlisting=AuctionListing.objects.get(id=listing_id))
        })


    bids = Bid.objects.filter(auctionlisting=litem).order_by('-bid').first()
    bidcount = Bid.objects.filter(auctionlisting=litem).count()

    bid_message=""

    if request.user.is_authenticated and bids != None:
        user = request.user
        if user == bids.user:
            bid_message = "Your bid is the current bid."


    return render(request,"auctions/detailed.html",{
        "listing_item":litem,
        "bidform":BidForm(),
        "commentform":CommentForm(),
        "comments":Comment.objects.all().filter(auctionlisting=AuctionListing.objects.get(id=listing_id)),
        "bidcount":bidcount,
        "bid":bids,
        "bid_message":bid_message
        
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
