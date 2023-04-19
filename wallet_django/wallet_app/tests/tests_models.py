from django.test import TestCase
from ..models import Master, Address


class MasterModelTests(TestCase):
    def test_unique_index(self):
        m1 = Master(coin='BTC', seed='1qaz', private_key='2wsx', chain_code='3edc')
        m1.save()
        m2 = Master(coin='BTC', seed='1qaz2', private_key='2wsx2', chain_code='3edc2')
        m2.save()
        count = Master.objects.filter(coin='BTC').count()
        self.assertEqual(count, 1)

    def test_save_none_exception(self):
        m = Master(coin='BTC')
        try:
            m.save()
            self.fail('Saved with None')
        except:
            pass


class AddressModelTests(TestCase):
    def test_unique_index(self):
        a1 = Address(id=0, coin='BTC', address='1qaz')
        a1.save()
        a2 = Address(id=0, coin='BTC', address='1qaz2')
        a2.save()
        count = Address.objects.filter(id=0).count()
        self.assertEqual(count, 1)

    def test_save_none_exception(self):
        a = Address(id=0)
        try:
            a.save()
            self.fail('Saved with None')
        except:
            pass

