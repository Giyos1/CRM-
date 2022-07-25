# Generated by Django 4.0.6 on 2022-07-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_payment_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='number_student',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]