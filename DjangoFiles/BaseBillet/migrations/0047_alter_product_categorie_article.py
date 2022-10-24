# Generated by Django 3.2 on 2022-10-22 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0046_event_recharge_cashless'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categorie_article',
            field=models.CharField(choices=[('N', 'Selectionnez une catégorie'), ('B', 'Billet'), ('P', "Pack d'objets"), ('R', 'Recharge cashless'), ('S', 'Recharge suspendue'), ('T', 'Vetement'), ('M', 'Merchandasing'), ('A', 'Adhésions et abonnements'), ('D', 'Don'), ('F', 'Reservation gratuite')], default='N', max_length=3, verbose_name="Type d'article"),
        ),
    ]
