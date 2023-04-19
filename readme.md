# Wallet

Implementation of simple REST API for generating valid cryptocurrency addresses and displaying them.

This is example for crypto wallet. The repository include two web frameworks: Flask, Django. 
Flask was used for developing rapid prototype. While Django for example closer to production.

The API provide:
- Generate master keys - retrieve coin identify (e.g. BTC), and generate master keys for that coin.
- Generate address - retrieve coin identify (e.g. BTC), and generate new address from the maser keys. The address stored in the database with associated integer ID.
- List address - list of all the addresses generated.
- Retrieve address - takes an ID, and returns the corresponding address as stored in the database.

There is index HTML page linking for the different API calls.
The return format for the API is in JSON format.

The code was developed and tested on Kubuntu 22.04.


## Dependencies

- Flask (for wallet_flask)
- Django (for wallet_django)
- Bitcoin
- Web3


## Design database tables

Database user is Sqlite3 for this example. The database have 2 tables. 
First table "Master" - hold the keys used to generate other keys.
The second table "Address" - hold the generated addresses.

1. Master
    - coin (string)
    - seed (string)
    - private_key (string)
    - chain_code (string)

2. Address
    - id (integer)
    - coin (string)
    - address (string)


## Clone and setup development environment

In empty folder run the next commends:
```
git clone git@github.com:yohanansivan/wallet.git . 
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

## Flask setup

Flask create database:
```
cd wallet_flask
python setup.py
```

Flask run debug server (http://127.0.0.1:5000):
```
python app.py
```


## Django setup

```
cd wallet_django
python manage.py makemigrations wallet_app
python manage.py migrate
```

Run debug server(http://127.0.0.1:8000/wallet_app):
```
python manage.py runserver
```

Run tests:
```
python manage.py test wallet_app
```


## Steps to support more coins

1. Add coin in the Coin Enum
2. Create child class Wallet (e.g. WalletXYZ)
3. Implement the methods:
  - generate_master
  - derivate_child_private_key
  - generate_address
4. Edit the function get_wallet
5. Edit the tests at wallet_app/tests/


## What is needed for implementing the next steps

- signing transactions
- User authentication

## Open questions

- How would you back up your private keys?
- How should a teammate add support for a new coin to the API?
- What is needed for implementing the next steps, such as signing transactions?
- The format you’ve chosen for inputs and outputs of the API


## Latest changes

- [x] Flask - add index page
- [x] Flask - add return json
- [x] Django - add index page
- [x] Django - add the wallet logic
- [x] Django - add comments to functions, classes
- [x] Django - add to wallet.py type hints
- [x] Django - create tests
- [x] Add python "requirement.txt" file
- [x] Add installation instruction
- [x] Add description how to add other coin


## Todo list

- [ ] Django - add logging
- [ ] Add description of how the wallet work (with diagrams)
- [ ] List task needed to be done to have full wallet (e.g. user authentication)
- [ ] Django - change the use of SECRET_KEY
- [ ] Answer how to securely store the private keys in the database? Maybe an option is to use the user password to create a key that can decrypt the coins private keys
- [ ] Flask - add try and except when connecting to database




## References

Bitcoin:
- https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch04.html

Wallet:
- https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

Django:
- https://docs.djangoproject.com/en/4.2/intro/install

Check valid address
- https://www.blockchain.com/explorer/addresses/eth/0xca947cafa98c1bf40d9d1d2c5bc83fddae6698d3


