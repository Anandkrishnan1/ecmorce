# Generated by Django 4.1.2 on 2022-10-26 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cont_tb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_NAME', models.CharField(max_length=255)),
                ('user_EMAIL', models.CharField(max_length=255)),
                ('user_PHNO', models.CharField(max_length=10)),
                ('usre_MSG', models.CharField(max_length=255)),
            ],
        ),
    ]
