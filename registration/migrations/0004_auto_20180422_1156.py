# Generated by Django 2.0.2 on 2018-04-22 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20180416_1801'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email',)},
        ),
    ]