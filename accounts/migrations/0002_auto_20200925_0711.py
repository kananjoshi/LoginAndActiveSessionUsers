# Generated by Django 2.0.7 on 2020-09-25 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='discription',
            new_name='description',
        ),
    ]