# Generated by Django 3.0.6 on 2020-08-23 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings_bid_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='added_by', to=settings.AUTH_USER_MODEL)),
                ('added_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='added_item', to='auctions.AuctionListings')),
            ],
        ),
    ]