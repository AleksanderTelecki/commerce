# Generated by Django 3.2.8 on 2021-11-19 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auctionlisting_closedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='closeDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]