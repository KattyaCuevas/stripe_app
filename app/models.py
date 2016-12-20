from django.db import models
from django.contrib.auth.models import AbstractUser
import webapp.settings as settings
import datetime
import stripe

# Create your models here.
stripe.api_key = settings.STRIPE_SECRET
class StripeUser(AbstractUser):
    stripe_id = models.CharField(max_length=20)
    plan = models.CharField(max_length=100)

    def __str__(self):
        return self.get_full_name()

    def create_account(self, stripe_token):
        stripe_customer = stripe.Customer.create(email=self.email, source=stripe_token)
        self.stripe_id = stripe_customer['id']
        self.save()

    def subscribe(self, plan):
        new_plan = stripe.Subscription.create(customer=self.stripe_id, plan=plan)
        self.plan = new_plan
        self.save()

class Payment(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    user = models.ForeignKey(StripeUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)
