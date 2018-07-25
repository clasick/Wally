from django.contrib import admin

# Register your models here.

from .models import Wallet, Profile, CreditCard, Transcation, Product

admin.site.register(Wallet)
admin.site.register(CreditCard)
admin.site.register(Transcation)
admin.site.register(Profile)
admin.site.register(Product)
