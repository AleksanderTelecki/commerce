from django.urls import path

from . import views

urlpatterns = [
    path("auction/", views.index, name="index"),
    path("auction/filter/<str:filter>",views.sidebar_filter,name="filter"),
    path("auction/<int:listing_id>",views.showListing,name="showListing"),
    path("auction/addtowatch/<int:listing_id>",views.addToWatch,name="addToWatch"),
    path("auction/createlisting",views.createListing,name="createListing"),
    path("auction/search",views.search,name="search"),
    path("auction/watchlist",views.watchList,name="watchList"),
    path("auction/mylistings",views.mylistings,name="mylistings"),
    path("auction/mylistings/close/<int:listing_id>",views.closelisting,name="closelisting"),
    path("auction/login", views.login_view, name="login"),
    path("auction/logout", views.logout_view, name="logout"),
    path("auction/register", views.register, name="register")
]
