# Generated by Django 4.2.3 on 2023-07-24 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_product_stock_variations_img1_variations_img2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variations',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='category.product'),
        ),
    ]
