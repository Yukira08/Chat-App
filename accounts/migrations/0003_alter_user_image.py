# Generated by Django 4.0 on 2021-12-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='pic.jpg', upload_to='profile_pics/'),
        ),
    ]
