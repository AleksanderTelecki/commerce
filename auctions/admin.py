from django.contrib import admin

# Register your models here.

from .models import User,Category,AuctionListing,Comment,Bid

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id","categoryName")


admin.site.register(User)
admin.site.register(Category,CategoriesAdmin)
admin.site.register(AuctionListing)
admin.site.register(Comment)
admin.site.register(Bid)

