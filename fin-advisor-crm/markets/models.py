from django.db import models
import constants as cons

# Create your models here.
class PublicCompanies(models.Model):
    """
    Information on listed companies.
    """

    # Fields
    ticker = models.CharField(
        max_length=cons.CHARACTER_MAX_LENGTH, 
        primary_key=True
    )
    name = models.CharField(
        max_length=cons.LARGE_CHARACTER_MAX_LENGTH
    )
    industry = models.CharField(
        max_length=cons.LARGE_CHARACTER_MAX_LENGTH
    )
    sector = models.CharField(
        max_length=cons.LARGE_CHARACTER_MAX_LENGTH
    )
    description = models.TextField()
  
    class Meta:
        ordering = ["ticker"]
    
    def __str__(self) -> str:
        return f"ticker: {self.ticker}, name: {self.name}"



class DailyTrades(models.Model):
    """
    Raw daily trading data for all stocks on the GSE. 
    """

    # Fields
    date = models.DateField()
    ticker = models.ForeignKey(
        PublicCompanies, 
        on_delete=models.PROTECT
    )
    price = models.DecimalField(
        max_digits=cons.MAX_DIGITS,
        decimal_places=cons.DECIMAL_PLACES
    )
    change = models.DecimalField(
        max_digits=cons.MAX_DIGITS,
        decimal_places=cons.DECIMAL_PLACES
    )
    volume = models.BigIntegerField()

    class Meta:
        ordering = ["date", "ticker"]
        unique_together = ["date", "ticker"]

    def __str__(self) -> str:
        return f"{super().__str__()}, name: {self.date}, ticker: {self.ticker}"



class EquityTrades(models.Model):
    """
    Table for persisting data to web application.
    """

    # Fields
    date = models.DateField()
    ticker = models.ForeignKey(
        PublicCompanies, 
        on_delete=models.PROTECT
    )
    price = models.DecimalField(
        max_digits=cons.MAX_DIGITS,
        decimal_places=cons.DECIMAL_PLACES
    )
    change = models.DecimalField(
        max_digits=cons.MAX_DIGITS,
        decimal_places=cons.DECIMAL_PLACES
    )
    volume = models.BigIntegerField()
    name = models.CharField(
        max_length=cons.LARGE_CHARACTER_MAX_LENGTH
    )
    industry = models.CharField(
        max_length=cons.LARGE_CHARACTER_MAX_LENGTH
    )    
    sector = models.CharField(
        max_length=cons.LARGE_CHARACTER_MAX_LENGTH
    )

    class Meta:
        ordering = ["date", "ticker"]
        unique_together = ["date", "ticker"]
    
    def __str__(self) -> str:
        return f"{super().__str__()}, date: {self.date}, ticker: {self.ticker}"



