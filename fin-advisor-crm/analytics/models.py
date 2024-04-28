from django.db import models

from main.models import Account, Security
import constants as const


# Create your models here.
class SecurityPrice(models.Model):
    securityid = models.ForeignKey(Security, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES
    )
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.securityid} - {self.date} - {self.price}"

    class Meta:
        unique_together = ["securityid", "date"]


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE, blank=True)
    trade_date = models.DateField()

    transaction_type = models.CharField(
        choices=const.TRANSACTION_TYPE_CHOICES,
        max_length=const.CHARACTER_MAX_LENGTH,
        blank=False,
    )
    transaction_quantity = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES, blank=True
    )
    transaction_amount = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES
    )
    transaction_id = models.CharField(
        max_length=const.CHARACTER_MAX_LENGTH, validators=[const.ALPHANUMERIC]
    )
    comment = models.CharField(max_length=const.LARGE_CHARACTER_MAX_LENGTH)

    def __str__(self) -> str:
        return f"{self.transaction_id}"

    class Meta:
        unique_together = ["transaction_id"]


class Position(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    date = models.DateField()
    market_value = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES, null=True
    )
    quantity = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES
    )

    def __str__(self) -> str:
        return f"Position - {self.account}|{self.security}|{self.date}"

    class Meta:
        unique_together = ["account", "security", "date"]


class EntityTrend(models.Model):
    entity = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    date = models.DateField()
    total_portfolio_value = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES
    )

    def __str__(self) -> str:
        return f"Position - {self.entity}|{self.date}"

    class Meta:
        unique_together = ["entity", "date"]
