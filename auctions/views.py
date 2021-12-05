from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,AuctionListing,Comment,Bid

class SelectForm(forms.Form):
    select = forms.ModelChoiceField(queryset=Category.objects.all(),required=False)
    maxprice = forms.FloatField(required=False)

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


def sidebar_filter(request,filter):

    query = QueryDict(query_string=filter)

    stringCategoryId = query.get("select",'')
    stringMaxPrice = query.get("maxprice",'')


    categoryId =int(stringCategoryId) if stringCategoryId != 'None' else 9 
    maxprice =float(stringMaxPrice) if stringMaxPrice != 'None' else None  

    form = SelectForm(initial = {'select': Category.objects.get(id=categoryId),'maxprice':maxprice })
    
    if categoryId == 9 or categoryId == None:

        if maxprice is not None:
            auctionquery = AuctionListing.objects.all().filter(startingPrice__lte = maxprice)

        return render(request,"auctions/index.html",{
        "auctions":auctionquery,
        "selectform":form

    })


    if maxprice is None:
        auctionquery = AuctionListing.objects.all().filter(category=categoryId)
    else:
        auctionquery = AuctionListing.objects.all().filter(category=categoryId).filter(startingPrice__lte = maxprice)

    return render(request,"auctions/index.html",{
        "auctions":auctionquery,
        "selectform":form

    })


def showListing(request,listing_id):

    
    try:
        litem=AuctionListing.objects.get(id=listing_id)
    except AuctionListing.DoesNotExist:
        litem = None


    if litem is None:
        return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":SelectForm()
        })

    return render(request,"auctions/detailed.html",{
        "listing_item":litem
        
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
