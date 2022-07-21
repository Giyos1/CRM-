from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


def validate_price(value):
    pass


class Course(models.Model):
    name = models.CharField(max_length=200)
    total_price = models.IntegerField()
    channel_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Account(models.Model):
    account_id = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='account')

    def __str__(self):
        return f"{self.username}({self.course.name})"


class Payment(models.Model):
    price = models.IntegerField()
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='payment')
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.username

