# Generated by Django 4.1.2 on 2022-10-26 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0002_cont_tb'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cont_tb',
            old_name='usre_MSG',
            new_name='user_MSG',
        ),
    ]