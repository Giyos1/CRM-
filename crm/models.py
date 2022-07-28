from django.db import models
from django.utils import timezone


def validate_price(value):
    pass


class DeletedManager(models.Manager):

    def get_queryset(self):
        return super(DeletedManager,
                     self).get_queryset() \
            .filter(delete=False)


class Course(models.Model):
    name = models.CharField(max_length=200)
    total_price = models.IntegerField()
    channel_id = models.CharField(max_length=200)
    lesson_number = models.IntegerField()
    number_student = models.IntegerField(default=1)

    @property
    def active_month(self):
        return int(self.lesson_number / 12) + 1

    def __str__(self):
        return self.name


class Account(models.Model):
    account_id = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='account')
    join = models.DateField(default=timezone.now)
    left = models.DateField(default=timezone.now)
    oquvchi_narxi = models.IntegerField(null=True, blank=True)
    start_course = models.IntegerField(null=True, blank=True, default=1)
    delete = models.BooleanField(default=False)
    delete_cause = models.TextField(null=True, blank=True, default=' ')
    objects = models.Manager()
    nodeleted = DeletedManager()

    @property
    def tolov_oyi(self):
        # print(self.course.active_month - self.start_course)
        return (self.course.active_month - self.start_course) + 1

    @property
    def qarzdorlik(self):
        tolashikerakli_summa = self.tolov_oyi * self.oquvchi_narxi
        tolangan_summa = 0
        payments = self.payment.all()
        for p in payments:
            tolangan_summa += p.price
        return tolashikerakli_summa - tolangan_summa

    def __str__(self):
        return f"{self.username}({self.course.name})"


class Payment(models.Model):
    title = models.TextField(default='Kurs uchun tolov')
    price = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.account.username
