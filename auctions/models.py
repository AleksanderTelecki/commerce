from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, FloatField
from django.core.validators import MinValueValidator
from django.db.models import Max


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.categoryName}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    startdate = models.DateTimeField(auto_now_add=False)
    closeDate = models.DateTimeField(blank=True,null=True)
    urlImage = models.URLField(max_length=200,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="auctionCategory")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner")
    
    
    Auction_STATUS = (
        ('S', 'Selling'),
        ('C', 'Closed')
    )
    
    status = models.CharField(max_length=1,choices=Auction_STATUS)
    
    def __str__(self):
        return f"Title: {self.title} Owner: {self.owner} Price: {self.getPrice()} Date: {self.startdate} Status: {self.status}"

    def getPrice(self):
        price=Bid.objects.filter(auctionlisting=self.id).aggregate(Max('bid'))['bid__max']
        if price is None:
            price=0
        return price

    def getFilteredByCategoryAndPrice(categoryId,max):
        if max is None:
            return AuctionListing.objects.all().filter(category=categoryId)


        if categoryId is None:
            auctionFilteredByID = AuctionListing.objects.all()
            maxlist=[]
            for item in auctionFilteredByID:
                if item.getPrice() <= max:
                    maxlist.append(item)

            return maxlist


        auctionFilteredByID = AuctionListing.objects.all().filter(category=categoryId)
        maxlist=[]
        for item in auctionFilteredByID:
            if item.getPrice() <= max:
                maxlist.append(item)
        
        return maxlist

        



  

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userComment")
    auctionlisting = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="auctionlistingComment")
    comment = models.TextField()

    def __str__(self):
        return f"User: {self.user} AuctionListing: {self.auctionlisting}"



class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userBids")
    auctionlisting = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="auctionlistingBids")
    bid = models.FloatField(validators=[
            MinValueValidator(1)
        ])
    def __str__(self):
        return f"User: {self.user} AuctionListing: {self.auctionlisting} Bid: {self.bid}"


class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userWatchlist")
    auctionlisting = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="auctionlistingItem")
    def __str__(self):
        return f"User: {self.user} AuctionListing: {self.auctionlisting}"





    




  