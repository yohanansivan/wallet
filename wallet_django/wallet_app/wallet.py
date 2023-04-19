'''Classes and functions for using wallet

Classes:
- Coin - enum for the different coins
- Wallet - abstract class for the wallet function
- WalletBTC - class for BitCoin wallet
- WalletETH - class for Ethereum wallet

Function:
- get_wallet - function return the type of wallet needed
'''

from enum import Enum
from abc import ABC, abstractmethod
import logging
import bitcoin
import hmac
import hashlib
from web3 import Web3


class Coin(Enum):
    BTC = 'BTC'
    ETH = 'ETH'


class Wallet(ABC):
    '''Abstract class for wallet'''

    @abstractmethod
    def generate_master(self) -> tuple[str, str, str]:
        '''Generate master keys

        Abstract method for generating master keys

        Returns:
          Implementation should return list of [seed, private_key, chain_code]
        '''
        pass

    @abstractmethod
    def derivate_child_private_key(self, private_key: str, chain_code: str, index: int) -> tuple[str, str]:
        '''Derivate child private keys from master keys

        Abstract method for derivate child keys from parent keys

        Args:
          - private_key - the master/parent private key
          - chain_code - the master/parent chain code
          - index - the child index

        Returns:
          Implementation should return list of [child_private_key, child_chain_code]
        '''
        pass

    @abstractmethod
    def generate_address(self, private_key: str) -> str:
        '''Generate address from private key

        Abstract method for derivate child keys from parent keys

        Args:
          - private_key

        Returns:
          Implementation should return address
        '''
        pass


class WalletBTC(Wallet):
    '''Class for BitCoin wallet'''

    def generate_master(self) -> tuple[str, str, str]:
        '''Generate master keys

        Method for generating master keys

        Returns:
          Implementation should return list of [seed, private_key, chain_code]
        '''
        seed = bitcoin.random_key()
        seed_bytes = bitcoin.safe_from_hex(seed)
        hash_bytes = hmac.digest(seed_bytes, b'', hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        private_key = hash[:64]
        chain_code = hash[64:]
        return seed, private_key, chain_code

    def derivate_child_private_key(self, private_key: str, chain_code: str, index: int) -> tuple[str, str]:
        '''Derivate child private keys from master keys

        Method for derivate child keys from parent keys

        Args:
          - private_key - the master/parent private key
          - chain_code - the master/parent chain code
          - index - the child index

        Returns:
          Implementation should return list of [child_private_key, child_chain_code]
        '''
        chain_code_bytes = bitcoin.safe_from_hex(chain_code)
        private_key_bytes = bitcoin.safe_from_hex(private_key)
        index_hex = bitcoin.encode(index, 16, 8)
        index_bytes = bitcoin.safe_from_hex(index_hex)
        hash_bytes = hmac.digest(chain_code_bytes, private_key_bytes + index_bytes, hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        child_private_key = hash[:64]
        child_chain_code = hash[64:]
        return child_private_key, child_chain_code

    def generate_address(self, private_key: str) -> str:
        '''Generate address from private key

        Method for derivate child keys from parent keys

        Args:
          - private_key

        Returns:
          Implementation should return address
        '''
        public_key = bitcoin.privkey_to_pubkey(private_key)
        address = bitcoin.pubkey_to_address(public_key)
        return address
    

class WalletETH(Wallet):
    '''Class for Ethereum wallet'''

    def generate_master(self) -> tuple[str, str, str]:
        '''Generate master keys

        Method for generating master keys

        Returns:
          Implementation should return list of [seed, private_key, chain_code]
        '''
        seed = bitcoin.random_key()
        seed_bytes = bitcoin.safe_from_hex(seed)
        hash_bytes = hmac.digest(seed_bytes, b'', hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        private_key = hash[:64]
        chain_code = hash[64:]
        return seed, private_key, chain_code

    def derivate_child_private_key(self, private_key, chain_code, index) -> tuple[str, str]:
        '''Derivate child private keys from master keys

        Method for derivate child keys from parent keys

        Args:
          - private_key - the master/parent private key
          - chain_code - the master/parent chain code
          - index - the child index

        Returns:
          Implementation should return list of [child_private_key, child_chain_code]
        '''
        chain_code_bytes = bitcoin.safe_from_hex(chain_code)
        private_key_bytes = bitcoin.safe_from_hex(private_key)
        index_hex = bitcoin.encode(index, 16, 8)
        index_bytes = bitcoin.safe_from_hex(index_hex)
        hash_bytes = hmac.digest(chain_code_bytes, private_key_bytes + index_bytes, hashlib.sha512)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        child_private_key = hash[:64]
        child_chain_code = hash[64:]
        return child_private_key, child_chain_code

    def generate_address(self, private_key) -> str:
        '''Generate address from private key

        Method for derivate child keys from parent keys

        Args:
          - private_key

        Returns:
          Implementation should return address
        '''
        public_key = bitcoin.privkey_to_pubkey(private_key)
        public_key_mod = public_key[2:]
        public_key_mod_bytes = bitcoin.safe_from_hex(public_key_mod)
        hash_bytes = Web3.keccak(public_key_mod_bytes)
        hash = bitcoin.bytes_to_hex_string(hash_bytes)
        address = '0x' + hash[-40:]
        return address


def get_wallet(coin) -> Wallet:
    '''Function to create the specific coin wallet

    Args:
      - coin - string exist in Coin Enum

    Returns:
      Return the instance of the wallet, or None of not exist
    '''
    wallet = None
    if coin == Coin.BTC.value:
        wallet = WalletBTC()
    if coin == Coin.ETH.value:
        wallet = WalletETH()
    return wallet


