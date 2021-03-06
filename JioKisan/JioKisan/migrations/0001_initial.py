# Generated by Django 2.1.3 on 2019-03-02 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consignment',
            fields=[
                ('ucid', models.AutoField(primary_key=True, serialize=False)),
                ('expected_delivery', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('TRANSIT', 'Transit'), ('COMPLETED', 'Completed')], default='PENDING', max_length=25)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FarmEntity',
            fields=[
                ('ufid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('measured_in', models.IntegerField()),
                ('MSP', models.IntegerField()),
                ('isFarmTool', models.BooleanField(default=False)),
                ('display_image', models.ImageField(blank=True, upload_to='fe_sample_images')),
            ],
        ),
        migrations.CreateModel(
            name='Produce',
            fields=[
                ('upid', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('isAssigned', models.BooleanField(default=False)),
                ('FE_info', models.ForeignKey(db_column='ufid', on_delete=django.db.models.deletion.CASCADE, to='JioKisan.FarmEntity')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('urid', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('isAssigned', models.BooleanField(default=False)),
                ('current_bid', models.IntegerField()),
                ('before_date', models.DateField()),
                ('FE_info', models.ForeignKey(db_column='ufid', on_delete=django.db.models.deletion.CASCADE, to='JioKisan.FarmEntity')),
            ],
        ),
        migrations.CreateModel(
            name='User_reg',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('phone_number', models.CharField(max_length=40, unique=True)),
                ('role', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=100)),
                ('PAN', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('licence_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('vehicle_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('vehicle_model', models.IntegerField(blank=True, default=None, null=True)),
                ('vehicle_capacity', models.IntegerField(blank=True, default=None, null=True)),
                ('organisation_name', models.CharField(blank=True, default=None, max_length=80, null=True)),
                ('bank_account_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('GST_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('isHired', models.BooleanField(blank=True, default=None, null=True)),
                ('path', models.CharField(blank=True, default=None, max_length=300, null=True)),
                ('available_capacity', models.IntegerField(blank=True, default=None, null=True)),
                ('current_address', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('position_latitude', models.FloatField(blank=True, default=None, null=True)),
                ('position_longitude', models.FloatField(blank=True, default=None, null=True)),
                ('isVerified', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='mandi_info',
            field=models.ForeignKey(db_column='PAN', on_delete=django.db.models.deletion.CASCADE, to='JioKisan.User_reg'),
        ),
        migrations.AddField(
            model_name='produce',
            name='farmer_info',
            field=models.ForeignKey(db_column='PAN', on_delete=django.db.models.deletion.CASCADE, to='JioKisan.User_reg'),
        ),
        migrations.AddField(
            model_name='consignment',
            name='prod',
            field=models.ForeignKey(db_column='upid', on_delete=django.db.models.deletion.CASCADE, to='JioKisan.Produce'),
        ),
        migrations.AddField(
            model_name='consignment',
            name='req',
            field=models.ForeignKey(db_column='urid', on_delete=django.db.models.deletion.CASCADE, to='JioKisan.Request'),
        ),
        migrations.AddField(
            model_name='consignment',
            name='truck',
            field=models.ForeignKey(blank=True, db_column='PAN', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='JioKisan.User_reg'),
        ),
    ]
