# Generated by Django 3.2 on 2023-01-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QrcodeCashless', '0007_alter_wallet_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartecashless',
            name='uuid',
            field=models.UUIDField(blank=True, db_index=True, editable=False, null=True, unique=True, verbose_name='Uuid'),
        ),
    ]
