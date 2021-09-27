# Generated by Django 2.2 on 2021-09-27 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0051_auto_20210927_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='id_stripe',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='lignearticle',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BaseBillet.Reservation'),
        ),
    ]
