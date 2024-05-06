from django.db import models
from django.contrib.auth.models import User

import constants as const

# Create your models here.


class Client(models.Model):
    clientid = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    name = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    date_opened = models.DateField()
    inception_date = models.DateField(null=True)
    client_type = models.CharField(
        choices=const.CLIENT_TYPE_CHOICES,
        max_length=const.CHARACTER_MAX_LENGTH,
        default="INDIVIDUAL",
    )
    advisor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.inception_date:
            self.inception_date = self.date_opened
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.clientid}"

    class Meta:
        unique_together = ["clientid"]


class Account(models.Model):
    accountid = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    clientid = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    date_opened = models.DateField()
    inception_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.inception_date:
            self.inception_date = self.date_opened
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.accountid}"

    class Meta:
        unique_together = ["accountid"]


class SecurityIndustry(models.Model):
    security_industry = models.CharField(
        max_length=const.CHARACTER_MAX_LENGTH, validators=[const.ALPHABET]
    )

    def __str__(self):
        return self.security_industry

    class Meta:
        unique_together = ["security_industry"]
        verbose_name = "Security Industry"
        verbose_name_plural = "Security Industries"


class SecuritySector(models.Model):
    security_sector = models.CharField(
        max_length=const.CHARACTER_MAX_LENGTH, validators=[const.ALPHABET]
    )

    def __str__(self):
        return self.security_sector

    class Meta:
        unique_together = ["security_sector"]
        verbose_name = "Security Sector"
        verbose_name_plural = "Security Sectors"


class Security(models.Model):
    securityid = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    name = models.CharField(max_length=const.CHARACTER_MAX_LENGTH)
    isin = models.CharField(max_length=const.CHARACTER_MAX_LENGTH, blank=True)
    ticker = models.CharField(max_length=const.CHARACTER_MAX_LENGTH, blank=True)
    unit_of_measure = models.DecimalField(
        max_digits=const.MAX_DIGITS, decimal_places=const.DECIMAL_PLACES, null=True
    )
    sector = models.ForeignKey(SecuritySector, on_delete=models.CASCADE)
    industry = models.ForeignKey(SecurityIndustry, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.securityid}"

    class Meta:
        unique_together = ["securityid"]
        verbose_name_plural = "Securities"
