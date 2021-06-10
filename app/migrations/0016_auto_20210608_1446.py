# Generated by Django 3.2 on 2021-06-08 09:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20210607_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingregistration',
            name='phone',
        ),
        migrations.AddField(
            model_name='addseed',
            name='qty',
            field=models.CharField(default='1 kg', max_length=50),
        ),
        migrations.AddField(
            model_name='seed',
            name='qty',
            field=models.CharField(default='1 kg', max_length=50),
        ),
        migrations.AddField(
            model_name='trainingregistration',
            name='mobile',
            field=models.CharField(default=1234567890, max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be of 10 digits.', regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be of 10 digits.', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='query',
            name='mobile',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be of 10 digits.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
