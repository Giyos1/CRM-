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
    else:
        number = Account.objects.count()
        number -= instance.number_student
        if number > 0:
            for i in range(number):
                Account.objects.create(
                    first_name='Unknown',
                    last_name='Unknown',
                    phone_number='Unknown',
                    course=instance
                )
