# Generated by Django 4.2.3 on 2023-07-26 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
        ('orders', '0003_orderitem_coupon_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='coupon_amount',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offers.coupon'),
        ),
    ]
