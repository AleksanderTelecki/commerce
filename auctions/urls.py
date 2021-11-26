from django.urls import path

from . import views

urlpatterns = [
    path("auction/", views.index, name="index"),
    path("auction/category/<int:selectedCategory>",views.selected_category,name="selected"),
    path("auction/login", views.login_view, name="login"),
    path("auction/logout", views.logout_view, name="logout"),
    path("auction/register", views.register, name="register")
]
