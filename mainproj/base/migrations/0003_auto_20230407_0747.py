# Generated by Django 3.2 on 2023-04-07 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20230407_0305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='update',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='update',
            new_name='updated',
        ),
    ]
