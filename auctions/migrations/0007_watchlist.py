# Generated by Django 3.2.8 on 2021-12-07 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_closedate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auctionlisting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctionlistingItem', to='auctions.auctionlisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userWatchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
