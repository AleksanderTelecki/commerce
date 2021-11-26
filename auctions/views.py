from unicodedata import category
from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,AuctionListing,Comment,Bid

class SelectForm(forms.Form):
    select = forms.ModelChoiceField(queryset=Category.objects.all())

def index(request):

    if  request.method == 'POST':
        form = SelectForm(request.POST)

        if form.is_valid():
            selected = form.cleaned_data['select']
            print(selected.id)
            url = reverse('selected', kwargs={'selectedCategory': selected.id })
            return HttpResponseRedirect(url)

    return render(request, "auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":SelectForm()
    })


def selected_category(request,selectedCategory):
    form = SelectForm(initial = {'select': Category.objects.get(id=selectedCategory) })
    
    if selectedCategory == 9:
        return render(request,"auctions/index.html",{
        "auctions":AuctionListing.objects.all(),
        "selectform":form

    })

    
    auctionquery = AuctionListing.objects.all().filter(category=selectedCategory)
    return render(request,"auctions/index.html",{
        "auctions":auctionquery,
        "selectform":form

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
