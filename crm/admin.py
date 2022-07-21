from django.contrib import admin
from .models import Course, Account, Payment


# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # list_display = ()
    pass

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # list_display = ()
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # list_display = ()
    pass
