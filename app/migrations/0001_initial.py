# Generated by Django 3.2 on 2021-05-24 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=35)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fertilizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=50)),
                ('img', models.ImageField(upload_to=None)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=35)),
                ('occupation', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=50)),
                ('img', models.ImageField(upload_to=None)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=50)),
                ('img', models.ImageField(upload_to=None)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Soil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=50)),
                ('img', models.ImageField(upload_to=None)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField()),
                ('college', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('duration', models.DurationField()),
                ('instruction', models.TextField()),
                ('problem', models.TextField()),
                ('date', models.DateField(auto_now=True)),
                ('fertilizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fertilizer')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.season')),
                ('seed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.seed')),
                ('soil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.soil')),
            ],
        ),
    ]
