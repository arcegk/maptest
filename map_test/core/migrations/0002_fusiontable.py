# Generated by Django 2.0 on 2018-08-07 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FusionTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.CharField(max_length=200, verbose_name='table id')),
            ],
        ),
    ]
