from django.test import TestCase
from ..models import Master, Address
from django.test import Client


class ViewsTests(TestCase):

    def get_response_json(self, response) -> dict | None:
        '''If response if json return dictionary
        
        Args:
          - response

        Return:
          If the response is json return dictionary of the json, else return None
        '''
        try:
            return response.json()
        except:
            return None

    def test_index(self):
        client = Client()
        response = client.get('/wallet_app/')
        self.assertEqual(response.status_code, 200)

    def test_generate_master(self):
        client = Client()

        # Check for BTC
        count = Master.objects.filter(coin='BTC').count()
        response = client.get('/wallet_app/generate_master/BTC')
        self.assertEqual(response.status_code, 200)
        d = self.get_response_json(response)
        if d == None:
            self.fail()
        else:
            if count == 0:
                self.assertEqual(d['status'], 'ok')
            else:
                self.assertEqual(d['status'], 'error')

        # Check for not supported coin
        response = client.get('/wallet_app/generate_master/XXX')
        self.assertEqual(response.status_code, 200)
        d = self.get_response_json(response)
        if d == None:
            self.fail()
        else:
            self.assertEqual(d['status'], 'error')


    def test_generate_address(self):
        client = Client()

        # Check for BTC
        count = Master.objects.filter(coin='BTC').count()
        response = client.get('/wallet_app/generate_address/BTC')
        self.assertEqual(response.status_code, 200)
        d = self.get_response_json(response)
        if d == None:
            self.fail()
        else:
            if count == 0:
                self.assertEqual(d['status'], 'error')
            else:
                self.assertEqual(d['status'], 'ok')

        # Check for not supported coin
        response = client.get('/wallet_app/generate_address/XXX')
        self.assertEqual(response.status_code, 200)
        d = self.get_response_json(response)
        if d == None:
            self.fail()
        else:
            self.assertEqual(d['status'], 'error')

    def test_list_address(self):
        client = Client()
        count = Address.objects.count()
        response = client.get('/wallet_app/list_address')
        self.assertEqual(response.status_code, 200)
        d = self.get_response_json(response)
        if d == None:
            self.fail()
        else:
            self.assertEqual(d['status'], 'ok')
            self.assertEqual(len(d['list_address']), count)

    def test_retrieve_address(self):
        client = Client()
        count = Address.objects.count()
        if count > 0:
            # Check exist index
            response = client.get(f'/wallet_app/retrieve_address/{count - 1}')
            self.assertEqual(response.status_code, 200)
            d = self.get_response_json(response)
            if d == None:
                self.fail()
            else:
                self.assertEqual(d['status'], 'ok')
            # Check not exist index
            response = client.get(f'/wallet_app/retrieve_address/{count}')
            self.assertEqual(response.status_code, 200)
            d = self.get_response_json(response)
            if d == None:
                self.fail()
            else:
                self.assertEqual(d['status'], 'error')
        else: # count == 0
            # Check not exist index
            response = client.get(f'/wallet_app/retrieve_address/0')
            self.assertEqual(response.status_code, 200)
            d = self.get_response_json(response)
            if d == None:
                self.fail()
            else:
                self.assertEqual(d['status'], 'error')


