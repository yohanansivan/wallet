from django.db import models


class Master(models.Model):
    coin = models.CharField(max_length=8, primary_key=True)
    seed = models.CharField(max_length=128)
    private_key = models.CharField(max_length=128)
    chain_code = models.CharField(max_length=128)

    def __str__(self):
        return f'coin:{self.coin} seed:{self.seed}'


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    coin = models.CharField(max_length=8)
    address = models.CharField(max_length=128)

    def __str__(self):
        return f'id:{self.id} coin:{self.coin} address:{self.address}'

