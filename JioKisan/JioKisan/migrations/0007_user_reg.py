# Generated by Django 2.1.5 on 2019-02-20 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JioKisan', '0006_auto_20181219_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_reg',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('phone_number', models.CharField(max_length=40)),
                ('role', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=100)),
                ('PAN', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
    ]
