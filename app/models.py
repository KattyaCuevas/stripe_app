from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class StripeUser(AbstractUser):
    stripe_id = models.CharField(max_length=20)
    plan = models.CharField(max_length=100)

class Payment(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    user = models.ForeignKey(StripeUser, on_delete=models.CASCADE)
