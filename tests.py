import requests
from unittest import TestCase
import hues


class Test(TestCase):
    def __init__(self):
        TestCase.__init__(self)
        self.__host = 'http://localhost:8004/'
        self.__purchases_host = self.__host + 'purchases'
        self.__shop_host = self.__host + 'shop'
        self.__factory_host = self.__host + 'factory'

    def upstate(self):
        try:
            shop_state = requests.get(self.__shop_host).status_code
            purchases_state = requests.get(self.__purchases_host).status_code
            factory_state = requests.get(self.__factory_host).status_code

            self.assertEqual(shop_state, 200)
            self.assertEqual(purchases_state, 200)
            self.assertEqual(factory_state, 200)
        except:
            raise AssertionError('Some service is down')

    




