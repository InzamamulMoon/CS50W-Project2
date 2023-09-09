from django.contrib import admin

from .models import listings,watchlists,proffer,Comments

class listingsAdmin(admin.ModelAdmin):
    list_display=("id","title","discription","image","Categories")
# Register your models here.
admin.site.register(listings, listingsAdmin)
admin.site.register(watchlists)
admin.site.register(proffer)
admin.site.register(Comments)



