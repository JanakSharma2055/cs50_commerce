from django.contrib import admin
from .models import User,AuctionListings,Bid,Comment,WatchList,Category

# Register your models here.
class AuctionListingsAdmin(admin.ModelAdmin):
    list_display=("title","price")
admin.site.register(User)

admin.site.register(AuctionListings,AuctionListingsAdmin)

admin.site.register(Bid)

admin.site.register(Comment)

admin.site.register(WatchList)

admin.site.register(Category)

