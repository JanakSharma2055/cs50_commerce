from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>",views.listingItem,name="listingItem"),
    path("create_listing",views.createListing,name="create_listing"),
    path("watchList",views.watchList,name="watch_list"),
    path("<int:item_id>/all_bids",views.allBids,name="all_bids")
 
    
]
