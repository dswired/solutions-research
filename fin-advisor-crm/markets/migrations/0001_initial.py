# Generated by Django 5.0.4 on 2024-05-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyPrivateEquityTrades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DailyRepoTrades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PublicCompanies",
            fields=[
                (
                    "ticker",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=200)),
                ("industry", models.CharField(max_length=200)),
                ("sector", models.CharField(max_length=200)),
                ("description", models.TextField()),
            ],
            options={
                "ordering": ["ticker"],
            },
        ),
        migrations.CreateModel(
            name="DailyBillCODPaperTrades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trade_date", models.DateField()),
                ("tenor", models.CharField(max_length=50)),
                ("security_type", models.CharField(max_length=50)),
                ("security_description", models.CharField(max_length=200)),
                ("isin", models.CharField(max_length=50)),
                ("opening_yield", models.DecimalField(decimal_places=5, max_digits=15)),
                ("closing_yield", models.DecimalField(decimal_places=5, max_digits=15)),
                ("opening_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("closing_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("volume_traded", models.BigIntegerField()),
                ("mumber_traded", models.BigIntegerField()),
                (
                    "day_high_yield",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                ("day_low_yeild", models.DecimalField(decimal_places=5, max_digits=15)),
                (
                    "day_high_price",
                    models.DecimalField(decimal_places=True, max_digits=15),
                ),
                ("day_low_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("days_to_maturity", models.BigIntegerField()),
                ("maturity_date", models.DateField()),
            ],
            options={
                "ordering": ["trade_date", "isin"],
                "unique_together": {("trade_date", "isin")},
            },
        ),
        migrations.CreateModel(
            name="DailyBondNoteTrades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trade_date", models.DateField()),
                ("tenor", models.CharField(max_length=50)),
                ("security_type", models.CharField(max_length=50)),
                ("security_description", models.CharField(max_length=200)),
                ("isin", models.CharField(max_length=50)),
                ("opening_yield", models.DecimalField(decimal_places=5, max_digits=15)),
                ("closing_yield", models.DecimalField(decimal_places=5, max_digits=15)),
                ("opening_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("closing_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("volume_traded", models.BigIntegerField()),
                ("mumber_traded", models.BigIntegerField()),
                (
                    "day_high_yield",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                ("day_low_yeild", models.DecimalField(decimal_places=5, max_digits=15)),
                (
                    "day_high_price",
                    models.DecimalField(decimal_places=True, max_digits=15),
                ),
                ("day_low_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("days_to_maturity", models.BigIntegerField()),
                ("maturity_date", models.DateField()),
            ],
            options={
                "ordering": ["trade_date", "isin"],
                "unique_together": {("trade_date", "isin")},
            },
        ),
        migrations.CreateModel(
            name="DailyPublicEquityTrades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trade_date", models.DateField()),
                ("ticker", models.CharField(max_length=200)),
                ("year_high", models.DecimalField(decimal_places=5, max_digits=15)),
                ("year_low", models.DecimalField(decimal_places=5, max_digits=15)),
                (
                    "previous_closing_price",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                ("opening_price", models.DecimalField(decimal_places=5, max_digits=15)),
                (
                    "last_transaction_price",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                ("closing_price", models.DecimalField(decimal_places=5, max_digits=15)),
                ("price_change", models.DecimalField(decimal_places=5, max_digits=15)),
                (
                    "closing_bid_price",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                (
                    "closing_offer_price",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                (
                    "total_shares_traded",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
                (
                    "total_value_traded",
                    models.DecimalField(decimal_places=5, max_digits=15),
                ),
            ],
            options={
                "ordering": ["trade_date", "ticker"],
                "unique_together": {("trade_date", "ticker")},
            },
        ),
    ]
