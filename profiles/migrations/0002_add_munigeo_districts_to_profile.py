# Generated by Django 2.0.5 on 2018-07-06 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='divisions_of_interest',
            field=models.ManyToManyField(blank=True, to='munigeo.AdministrativeDivision'),
        ),
    ]
