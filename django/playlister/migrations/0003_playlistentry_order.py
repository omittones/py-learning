# Generated by Django 2.1 on 2019-10-12 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlister', '0002_make_soruce_id_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlistentry',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
