# Generated by Django 3.0.6 on 2020-09-19 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='category', to='auctions.Category'),
        ),
    ]
