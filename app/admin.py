from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import StripeUser, Payment

@admin.register(StripeUser)
class StripeUser(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Extra'), {'fields': ('stripe_id', 'plan')}),
    )

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    pass
