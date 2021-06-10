# Generated by Django 3.2 on 2021-06-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210602_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='query',
            name='subject',
        ),
        migrations.AlterField(
            model_name='addseed',
            name='product_detail',
            field=models.CharField(default='No Details', max_length=500),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='city',
            field=models.CharField(default='Lucknow', max_length=32),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='country',
            field=models.CharField(default='India', max_length=32),
        ),
    ]
