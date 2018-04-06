from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.user.username.title() + "'s wallet"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    phone_no = models.CharField(max_length=10, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Transcation(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    amt = models.FloatField()
    timestamp = models.DateTimeField()


class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=100)
    cvv = models.CharField(max_length=3)
    number = models.CharField(max_length=16)
    exp_date = models.CharField(max_length=6)
