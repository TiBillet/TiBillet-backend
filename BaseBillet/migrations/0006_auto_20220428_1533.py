# Generated by Django 3.2 on 2022-04-28 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0005_alter_reservation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='activate_mailjet',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='email_confirm_template',
            field=models.IntegerField(default=3898061),
        ),
    ]
