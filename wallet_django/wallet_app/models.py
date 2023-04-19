from django.db import models


class Master(models.Model):
    coin = models.CharField(max_length=8, default=None, primary_key=True)
    seed = models.CharField(max_length=128, default=None, null=False)
    private_key = models.CharField(max_length=128, default=None, null=False)
    chain_code = models.CharField(max_length=128, default=None, null=False)

    def __str__(self):
        return f'coin:{self.coin} seed:{self.seed}'


class Address(models.Model):
    id = models.IntegerField(default=None, primary_key=True)
    coin = models.CharField(max_length=8, default=None, null=False)
    address = models.CharField(max_length=128, default=None, null=False)

    def __str__(self):
        return f'id:{self.id} coin:{self.coin} address:{self.address}'

