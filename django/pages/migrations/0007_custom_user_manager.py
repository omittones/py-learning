from django.db import migrations
from pages.models import CustomUserManager


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_customuser_age'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', CustomUserManager()),
            ],
        ),
    ]
