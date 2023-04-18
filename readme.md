# Wallet

## References

Bitcoin:
- https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch04.html

Wallet:
- https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

Django:
- https://docs.djangoproject.com/en/4.2/intro/install


## Flask

```
cd wallet_flask
python setup.py
python app.py
```


## Django

```
cd wallet_django
```

```
python manage.py runserver
```

```
python manage.py migrate
```

```
python manage.py makemigrations wallet_app
```

```
python manage.py migrate
```

```
python manage.py shell
```

```python
from wallet_app.models import Master, Address
print(Master.objects.all())
m = Master()
m.coin = 'BTC'
m.seed = '1qaz'
m.private_key = '2wsx'
m.chain_code = '3edc'
m.save()
print(Master.objects.all())
m = Master.objects.get(coin='BTC')
m.delete()
print(Master.objects.all())
```

## Todo

- Answer how to securely store the private keys in the database?

One option is to use the user password to create a key that can decrypt the coins private keys

- Needs to add try and except when connecting to database


