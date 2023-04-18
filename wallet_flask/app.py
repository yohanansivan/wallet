from flask import Flask
from datetime import datetime
import sqlite3
from enum import Enum
from abc import ABC, abstractmethod
import logging
import bitcoin
import hmac
import hashlib
from web3 import Web3


# === Tables ===
# Master - coin:str, seed:str, private_key:str, chain_code:str
# Address - id:int, coin:str, address:str


class Coin(Enum):
    BTC = 'BTC'
    ETH = 'ETH'


class Wallet(ABC):
    @abstractmethod
    def generate_master(self):
        pass

    @abstractmethod
    def derivate_child_private_key(self, private_key, chain_code, index):
        pass

    @abstractmethod
    def generate_address(self, private_key):
        pass


class WalletBTC(Wallet):
    def generate_master(self):
        seed = bitcoin.random_key()
        seed_bytes = bitcoin.safe_from_hex(seed)
        hash_bytes = hmac.digest(seed_bytes, b'', hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        private_key = hash[:64]
        chain_code = hash[64:]
        return seed, private_key, chain_code

    def derivate_child_private_key(self, private_key, chain_code, index):
        chain_code_bytes = bitcoin.safe_from_hex(chain_code)
        private_key_bytes = bitcoin.safe_from_hex(private_key)
        index_hex = bitcoin.encode(index, 16, 8)
        index_bytes = bitcoin.safe_from_hex(index_hex)
        hash_bytes = hmac.digest(chain_code_bytes, private_key_bytes + index_bytes, hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        child_private_key = hash[:64]
        child_chain_code = hash[64:]
        return child_private_key, child_chain_code

    def generate_address(self, private_key):
        public_key = bitcoin.privkey_to_pubkey(private_key)
        address = bitcoin.pubkey_to_address(public_key)
        return address
    

class WalletETH(Wallet):
    def generate_master(self):
        seed = bitcoin.random_key()
        seed_bytes = bitcoin.safe_from_hex(seed)
        hash_bytes = hmac.digest(seed_bytes, b'', hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        private_key = hash[:64]
        chain_code = hash[64:]
        return seed, private_key, chain_code

    def derivate_child_private_key(self, private_key, chain_code, index):
        chain_code_bytes = bitcoin.safe_from_hex(chain_code)
        private_key_bytes = bitcoin.safe_from_hex(private_key)
        index_hex = bitcoin.encode(index, 16, 8)
        index_bytes = bitcoin.safe_from_hex(index_hex)
        hash_bytes = hmac.digest(chain_code_bytes, private_key_bytes + index_bytes, hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        child_private_key = hash[:64]
        child_chain_code = hash[64:]
        return child_private_key, child_chain_code

    def generate_address(self, private_key):
        public_key = bitcoin.privkey_to_pubkey(private_key)
        public_key_mod = public_key[2:]
        public_key_mod_bytes = bitcoin.safe_from_hex(public_key_mod)
        hash_bytes = Web3.keccak(public_key_mod_bytes)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        address = '0x' + hash[-40:]
        return address


def get_wallet(coin):
    wallet = None
    if coin == Coin.BTC.value:
        wallet = WalletBTC()
    if coin == Coin.ETH.value:
        wallet = WalletETH()
    return wallet


app = Flask(__name__)
database = 'db.sqlite3'


@app.get('/')
def get_index():
    logging.debug('get_index')
    now = datetime.now()
    return f'[{now}] Hello from flask'


@app.get('/generate_master/<coin>')
def get_generate_master(coin):
    logging.debug('get_generate_master')
    now = datetime.now()
    wallet = get_wallet(coin)
    if wallet == None:
        return f'[{now}] Error coin {coin} not supported'
    # Check if coin exist
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM master WHERE coin == ?;", (coin,))
    fetched = res.fetchall()
    if len(fetched) != 0:
        con.close()
        return f'[{now}] Error master for {coin} already exist'
    # Generate new master key
    seed, private_key, chain_code = wallet.generate_master()
    res = cur.execute("INSERT INTO master (coin, seed, private_key, chain_code) \
                      VALUES (?, ?, ?, ?);", (coin, seed, private_key, chain_code))
    con.commit()
    con.close()
    return f'[{now}] Generated master keys for {coin}'


@app.get('/generate_address/<coin>')
def get_generate_address(coin):
    logging.debug('get_generate_address')
    now = datetime.now()
    wallet = get_wallet(coin)
    if wallet == None:
        return f'[{now}] Error coin {coin} not supported'
    # Get coin master keys
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute('SELECT private_key, chain_code FROM master \
                      WHERE coin = ?;', (coin,))
    fetched = res.fetchall()
    if len(fetched) != 1:
        con.close()
        return f'[{now}] Error coin do not have master keys'
    private_key, chain_code = fetched[0]
    # Count the number of rows as new index
    res = cur.execute("SELECT COUNT(id) FROM address;")
    index = res.fetchone()[0]
    # Generating address from masters
    child_private_key, child_chain_code = wallet.derivate_child_private_key(private_key, chain_code, index)
    child_address = wallet.generate_address(child_private_key)
    # Save the new address
    res = cur.execute("INSERT INTO address (id, coin, address) \
                      VALUES (?, ?, ?);", (index, coin, child_address))
    con.commit()
    con.close()
    return f'[{now}] Generated {child_address}'


@app.get('/list_address')
def get_list_address():
    logging.debug('get_list_address')
    now = datetime.now()
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("SELECT id, coin, address FROM address;")
    fetched = res.fetchall()
    return f'[{now}] Fetched {fetched}'


@app.get('/retrieve_address/<id>')
def get_retrieve_address(id):
    logging.debug('get_retrieve_address')
    now = datetime.now()
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("SELECT id, coin, address FROM address \
                      WHERE id == ?;", id)
    fetched = res.fetchall()
    if len(fetched) != 1:
        return f'[{now}] Error not found address id'
    return f'[{now}] Address: {fetched}'


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('main')
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()

# https://www.blockchain.com/explorer/addresses/eth/0xca947cafa98c1bf40d9d1d2c5bc83fddae6698d3


