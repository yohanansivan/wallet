from django.test import TestCase
from ..wallet import Coin, WalletBTC, WalletETH, get_wallet
import bitcoin


class WalletTests(TestCase):
    def test_get_wallet(self):
        wallet = get_wallet('BTC')
        self.assertEqual(type(wallet), WalletBTC)
        wallet = get_wallet('ETH')
        self.assertEqual(type(wallet), WalletETH)
        wallet = get_wallet('XXX')
        self.assertEqual(wallet, None)

    def test_generate_master(self):
        coins = [coin.value for coin in Coin]
        for coin in coins:
            wallet = get_wallet(coin)
            seed, private_key, chain_code = wallet.generate_master()
            self.assertEqual(type(seed), str)
            self.assertGreater(len(seed), 0)
            self.assertEqual(type(private_key), str)
            self.assertGreater(len(private_key), 0)
            self.assertEqual(type(chain_code), str)
            self.assertGreater(len(chain_code), 0)

    def test_derivate_child_private_key(self):
        coins = [coin.value for coin in Coin]
        private_key = bitcoin.random_key()
        chain_code = bitcoin.random_key()
        index = 42
        for coin in coins:
            wallet = get_wallet(coin)
            child_private_key, child_chain_code = wallet.derivate_child_private_key(private_key, chain_code, index)
            self.assertEqual(type(child_private_key), str)
            self.assertGreater(len(child_private_key), 0)
            self.assertEqual(type(child_chain_code), str)
            self.assertGreater(len(child_chain_code), 0)

    def test_generate_address(self):
        coins = [coin.value for coin in Coin]
        private_key = bitcoin.random_key()
        for coin in coins:
            wallet = get_wallet(coin)
            address = wallet.generate_address(private_key)
            self.assertEqual(type(address), str)
            self.assertGreater(len(address), 0)
        

