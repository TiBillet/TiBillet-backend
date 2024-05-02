# Generated by Django 3.2 on 2023-05-22 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0071_event_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#000000', max_length=7, verbose_name='Couleur du tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Nom du tag'),
        ),
    ]
