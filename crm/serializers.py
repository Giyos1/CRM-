from rest_framework import serializers, validators
from .models import Course, Account, Payment


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     c_id = self['course']
    #     a_id = self['id']
    #     account = Account.nodeleted.get(id=a_id)
    #     course = Course.objects.get(id=c_id)
    #     print(validated_data)
    #     print(1)
    #     if course.active_month < account.start_course:
    #         print(self['start_course'])
    #         self['start_course'] = course.active_month
    #     account = Account.objects.update_or_create(start_course=self['start_course'], **validated_data)
    #     return account


class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
