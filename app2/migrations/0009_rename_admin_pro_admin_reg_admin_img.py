# Generated by Django 4.1.2 on 2022-11-02 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0008_admin_reg_remove_reg_tb_user_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin_reg',
            old_name='Admin_pro',
            new_name='Admin_img',
        ),
    ]