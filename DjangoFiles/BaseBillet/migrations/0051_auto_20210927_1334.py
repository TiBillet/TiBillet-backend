# Generated by Django 2.2 on 2021-09-27 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0050_auto_20210927_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='categorie_article',
            field=models.CharField(choices=[('B', 'Billet'), ('P', "Pack d'objets"), ('R', 'Recharge cashless'), ('T', 'Vetement'), ('M', 'Merchandasing')], default='B', max_length=3, verbose_name='Status de la réservation'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='cadeau_adhesion',
            field=models.FloatField(default=0, help_text="Recharge cadeau a l'adhésion"),
        ),
        migrations.AlterField(
            model_name='lignearticle',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BaseBillet.Reservation'),
        ),
    ]
