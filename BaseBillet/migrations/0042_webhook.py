# Generated by Django 3.2 on 2022-10-18 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0041_auto_20221018_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('event', models.CharField(choices=[('RV', 'Réservation validée')], default='RV', max_length=2, verbose_name='Évènement')),
            ],
        ),
    ]
