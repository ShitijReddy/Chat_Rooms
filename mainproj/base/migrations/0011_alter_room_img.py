# Generated by Django 3.2 on 2023-04-20 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_room_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
