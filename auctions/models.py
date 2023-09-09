from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
 title=models.CharField(max_length=25)
 discription=models.CharField(max_length=500)
 image=models.CharField(max_length=600, blank=True)
 starting_bid=models.FloatField()
 bid=models.FloatField()
 owner=models.ForeignKey(User, on_delete=models.CASCADE)
 closing=models.BooleanField(default=False)
 Auction_Categories=[("FA","Fashion"),
                     ("TY","Toys"),
                     ("EL","Electronics"),
                     ("HO","Home")]
 Categories=models.CharField(choices=Auction_Categories, default='FA',max_length=12)

class Comments(models.Model):
    comments=models.CharField(max_length=250)
    item=models.ForeignKey(listings, on_delete=models.CASCADE)
    commenters=models.ForeignKey(User, on_delete=models.CASCADE, related_name="individual")

class proffer(models.Model):
   lisiting_bid=models.FloatField()
   treasure=models.ForeignKey(listings, on_delete=models.CASCADE)
   bidder=models.ForeignKey(User,on_delete=models.CASCADE, related_name="bidder")
   
class watchlists(models.Model):
   user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
   listing=models.ManyToManyField(listings, related_name="item")

