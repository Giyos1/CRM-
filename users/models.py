from django.db import models


# Create your models here.

class Sanalar(models.Model):
    dars = models.IntegerField(null=False)
    sana = models.TextField(null=False)
    from_id = models.TextField(null=False)
    to_id = models.TextField(null=False)


class Admins(models.Model):
    admin_id = models.TextField()
    group_id = models.TextField()
