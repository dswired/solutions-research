from django.db import models
import constants as cons


##########################################################################################
#################                       Equity Data                     ##################
##########################################################################################


class DailyPublicEquityTrades(models.Model):
    """
    Daily trading data for public equity securities trading on the ghana stock exchange.
    Data obtained from the Ghana Stock Exchange website:
    https://gse.com.gh/trading-and-data/#dailyshares
    """

    # Fields
    trade_date = models.DateField()
    ticker = models.CharField(max_length=cons.LARGE_CHARACTER_MAX_LENGTH)
    year_high = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    year_low = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    previous_closing_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    opening_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    last_transaction_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    price_change = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_bid_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_offer_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    total_shares_traded = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    total_value_traded = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )

    class Meta:
        ordering = ["trade_date", "ticker"]
        unique_together = ["trade_date", "ticker"]

    def __str__(self) -> str:
        return f"{super().__str__()}, date: {self.trade_date}, ticker: {self.ticker}"


class DailyPrivateEquityTrades(models.Model): ...


class PublicCompanies(models.Model):
    """
    Information on listed companies. Manually generated
    """

    # Fields
    ticker = models.CharField(max_length=cons.CHARACTER_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=cons.LARGE_CHARACTER_MAX_LENGTH)
    industry = models.CharField(max_length=cons.LARGE_CHARACTER_MAX_LENGTH)
    sector = models.CharField(max_length=cons.LARGE_CHARACTER_MAX_LENGTH)
    description = models.TextField()

    class Meta:
        ordering = ["ticker"]

    def __str__(self) -> str:
        return f"ticker: {self.ticker}, name: {self.name}"


##########################################################################################
#################                   Fixed Income Data                   ##################
##########################################################################################
class DailyBondNoteTrades(models.Model):
    """
    Daily trading data for long-term fixed income securities - Government & Corporate
    Bonds, & Government Notes on the Ghana Fixed Income Market. Data obtained from
    Ghana Fixed Income Markets: https://gfim.com.gh/daily-trading-reports/.
    """

    trade_date = models.DateField()
    tenor = models.CharField(
        max_length=cons.CHARACTER_MAX_LENGTH,
    )
    security_type = models.CharField(max_length=cons.CHARACTER_MAX_LENGTH)
    security_description = models.CharField(max_length=cons.LARGE_CHARACTER_MAX_LENGTH)
    isin = models.CharField(max_length=cons.CHARACTER_MAX_LENGTH)
    opening_yield = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_yield = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    opening_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    volume_traded = models.BigIntegerField()
    mumber_traded = models.BigIntegerField()
    day_high_yield = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    day_low_yeild = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    day_high_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=True
    )
    day_low_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    days_to_maturity = models.BigIntegerField()
    maturity_date = models.DateField()

    class Meta:
        ordering = ["trade_date", "isin"]
        unique_together = ["trade_date", "isin"]

    def __str__(self) -> str:
        return f"{super().__str__()}, name: {self.trade_date}, ticker: {self.isin}"


class DailyBillCODPaperTrades(models.Model):
    """
    Daily trading data for medium-term fixed income securities - treasury bills,
    certificates of deposit, commercial papers. Data obtained from Ghana Fixed Income
    Markets: https://gfim.com.gh/daily-trading-reports/
    """

    trade_date = models.DateField()
    tenor = models.CharField(
        max_length=cons.CHARACTER_MAX_LENGTH,
    )
    security_type = models.CharField(max_length=cons.CHARACTER_MAX_LENGTH)
    security_description = models.CharField(max_length=cons.LARGE_CHARACTER_MAX_LENGTH)
    isin = models.CharField(max_length=cons.CHARACTER_MAX_LENGTH)
    opening_yield = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_yield = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    opening_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    closing_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    volume_traded = models.BigIntegerField()
    mumber_traded = models.BigIntegerField()
    day_high_yield = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    day_low_yeild = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    day_high_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=True
    )
    day_low_price = models.DecimalField(
        max_digits=cons.MAX_DIGITS, decimal_places=cons.DECIMAL_PLACES
    )
    days_to_maturity = models.BigIntegerField()
    maturity_date = models.DateField()

    class Meta:
        ordering = ["trade_date", "isin"]
        unique_together = ["trade_date", "isin"]

    def __str__(self) -> str:
        return f"{super().__str__()}, name: {self.trade_date}, ticker: {self.isin}"


class DailyRepoTrades(models.Model):
    """
    Daily trading data for short-term fixed income securities - Repos. Data obtained
    from Ghana Fixed Income Markets: https://gfim.com.gh/daily-trading-reports/
    """

    ...
