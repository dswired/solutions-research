# Generated by Django 5.0.4 on 2024-05-13 03:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("markets", "0002_alter_dailypublicequitytrades_closing_bid_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="closing_bid_price",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="closing_offer_price",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="closing_price",
            field=models.DecimalField(
                decimal_places=5, default=django.utils.timezone.now, max_digits=15
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="last_transaction_price",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="previous_closing_price",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="price_change",
            field=models.DecimalField(
                decimal_places=5, default=django.utils.timezone.now, max_digits=15
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="total_shares_traded",
            field=models.DecimalField(
                decimal_places=5, default=django.utils.timezone.now, max_digits=15
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="total_value_traded",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="year_high",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dailypublicequitytrades",
            name="year_low",
            field=models.DecimalField(
                blank=True, decimal_places=5, default=None, max_digits=15, null=True
            ),
        ),
    ]
