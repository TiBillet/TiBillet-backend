# Generated by Django 3.2 on 2023-05-23 11:48

from django.db import migrations, models
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0073_auto_20230523_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='adhesion_obligatoire',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='button_adhesion',
        ),
        migrations.AlterField(
            model_name='configuration',
            name='adress',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='city',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='long_description',
            field=models.TextField(blank=True, null=True, verbose_name='Description longue'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='map_img',
            field=stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], variations={'fhd': (1920, 1920), 'hdr': (720, 720), 'med': (480, 480), 'thumbnail': (150, 90)}, verbose_name='Carte géographique'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='postal_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='Code postal'),
        ),
        migrations.AlterField(
            model_name='event',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Publier'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categorie_article',
            field=models.CharField(choices=[('N', 'Selectionnez une catégorie'), ('B', 'Billet'), ('P', "Pack d'objets"), ('R', 'Recharge cashless'), ('S', 'Recharge suspendue'), ('T', 'Vetement'), ('M', 'Merchandasing'), ('A', 'Adhésions associative'), ('B', 'Abonnement'), ('D', 'Don'), ('F', 'Reservation gratuite')], default='N', max_length=3, verbose_name='Type de produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='send_to_cashless',
            field=models.BooleanField(default=False, help_text='Produit qui doit être envoyé pour une comptabilité au cashless. Ex : Adhésions', verbose_name='Envoyer au cashless'),
        ),
    ]
