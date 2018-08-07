# Generated by Django 2.0 on 2018-08-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.CharField(max_length=100, verbose_name='latitude')),
                ('lon', models.CharField(max_length=100, verbose_name='longitude')),
                ('address', models.CharField(max_length=125, verbose_name='address')),
            ],
        ),
    ]