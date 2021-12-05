from django.urls import path

from . import views

urlpatterns = [
    path("auction/", views.index, name="index"),
    path("auction/filter/<str:filter>",views.sidebar_filter,name="filter"),
    path("auction/<int:listing_id>",views.showListing,name="showListing"),
    path("auction/login", views.login_view, name="login"),
    path("auction/logout", views.logout_view, name="logout"),
    path("auction/register", views.register, name="register")
]
