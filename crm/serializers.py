from rest_framework import serializers, validators
from .models import Course, Account


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        depth = 1