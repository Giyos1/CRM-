from django.dispatch import receiver
from django.db.models.signals import post_save
from crm.models import Course, Account


@receiver(post_save, sender=Course)
def creat_course(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.number_student):
            Account.objects.create(
                first_name='Unknown',
                last_name='Unknown',
                phone_number='Unknown',
                course=instance
            )
    elif not created:
        number = Account.objects.filter(course=instance).count()
        number = instance.number_student - number
        if number > 0:
            for i in range(number):
                Account.objects.create(
                    first_name='Unknown',
                    last_name='Unknown',
                    phone_number='Unknown',
                    course=instance
                )
        # print(instance.lesson_number)
        # if instance.lesson_number == 120:
        #     c = Course.objects.filter(id=instance.id)
        #     c.is_active = False
        #     print(c.is_active)
        #     c.save()


@receiver(post_save, sender=Account)
def create_account(sender, instance, created, **kwargs):
    if created:
        instance.start_course = instance.course.lesson_number / 12 + 1
        instance.oquvchi_narxi = instance.course.total_price
        instance.save()
