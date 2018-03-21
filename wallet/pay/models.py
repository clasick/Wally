from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    def __str__(self):
        return self.user.username.title() + "'s wallet"
