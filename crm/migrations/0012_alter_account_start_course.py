# Generated by Django 4.0.6 on 2022-07-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_account_oquvchi_narxi_account_start_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='start_course',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]