import requests
import unittest


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.__host = 'https://rulab.icyftl.ru/'
        self.__purchases_host = self.__host + 'purchases'
        self.__shop_host = self.__host + 'shop'
        self.__factory_host = self.__host + 'factory'
        self.__shop_password = 'lol'

    def test_upstate(self):
        try:
            shop_state = requests.get(self.__shop_host).status_code
            purchases_state = requests.get(self.__purchases_host).status_code
            factory_state = requests.get(self.__factory_host).status_code

            self.assertEqual(shop_state, 200)
            self.assertEqual(purchases_state, 200)
            self.assertEqual(factory_state, 200)
        except Exception as e:
            raise AssertionError('Some services are down or something went wrong\n' + str(e))

    def test_create_shop(self):
        try:
            shop = requests.post(self.__shop_host + '/create', json={
                "name": "UTest",
                "address": "UTest",
                "number": "79167031312"
            }, headers={'XXX-CODE': self.__shop_password})

            self.assertEqual(shop.status_code, 201)
        except:
            raise AssertionError('Shop service is down or something went wrong')

    def test_add_items(self):
        try:
            shop = requests.put(self.__shop_host + '/1/add_items', json={
                "items": [
                    {
                        "name": "TestCake",
                        "category": "TestCakes",
                        "count": 100
                    }
                ]
            }, headers={'XXX-CODE': self.__shop_password})

            self.assertEqual(shop.status_code, 201)
        except Exception as e:
            raise AssertionError('Shop service is down or something went wrong\n' + str(e))

    def test_new_purchase(self):
        try:
            slots = requests.get(self.__shop_host + '/1/get_slots').json()
            self.assertTrue(any([x['name'] == 'testcake' for x in slots['response']['result']]))
            slots = slots['response']['result']
            slot = None
            for x in slots:
                if x['name'] == 'testcake':
                    slot = x
                    break

            r = requests.post(self.__shop_host + '/1/new_purchase', json={

                "slot_id": slot['id'],
                "count": 1,
                "user_id": 1,
                "method": "card"

            })

            self.assertEqual(r.status_code, 200)

            r = requests.post(self.__shop_host + '/1/new_purchase', json={

                "slot_id": slot['id'],
                "count": 100,
                "user_id": 1,
                "method": "card"

            })

            self.assertEqual(r.status_code, 424)
        except Exception as e:
            raise AssertionError('Shop service is down or something went wrong\n' + str(e))

if __name__ == '__main__':
    unittest.main()
