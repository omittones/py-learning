# Generated by Django 2.1 on 2019-10-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlister', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='source_specific_id',
            field=models.CharField(max_length=2000, blank=True, null=True),
        ),
    ]