from django.contrib.auth.models import AbstractUser
from django.db import models
import math
from django.utils import timezone


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
    pub_date=models.DateTimeField(auto_now_add=True)
    commented_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="commented_by")
    commented_on=models.ForeignKey(AuctionListings,on_delete=models.CASCADE,related_name="commented_on")

    def __str__(self):
        return f"{self.comment}"
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.pub_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

class WatchList(models.Model):
    added_by=models.ForeignKey(User ,on_delete=models.CASCADE,related_name="added_by")
    added_item=models.ForeignKey(AuctionListings,on_delete=models.CASCADE,related_name="added_item")

