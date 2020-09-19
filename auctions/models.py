from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name=models.CharField(default="none",blank=True,max_length=100)
    def __str__(self):
        return f"{self.name}"


class AuctionListings(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    img_url=models.URLField()
    description=models.TextField()
    #associated user for the post
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    date=models.DateTimeField(auto_now_add=True)
    bid_active=models.BooleanField(default=True)
    category=models.ManyToManyField(Category,blank=True,related_name="category")
    def __str__(self):
        return f"{self.title}\n {self.description}"

    

class Bid(models.Model):
    bid_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidder")
    price=models.FloatField()
    bid_on=models.ForeignKey(AuctionListings,
    on_delete=models.CASCADE,related_name="bid_on")


class Comment(models.Model):
    comment=models.TextField()
    commented_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="commented_by")
    commented_on=models.ForeignKey(AuctionListings,on_delete=models.CASCADE,related_name="commented_on")

    def __str__(self):
        return f"{self.commented_by.username}:{self.comment}"

class WatchList(models.Model):
    added_by=models.ForeignKey(User ,on_delete=models.CASCADE,related_name="added_by")
    added_item=models.ForeignKey(AuctionListings,on_delete=models.CASCADE,related_name="added_item")

