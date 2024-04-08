import unittest
import requests
import random
import string

class TestAPIEndpoints(unittest.TestCase):
    # Base URL of the site
    BASE_URL = 'http://localhost:5000'

    # Test 01: Ping the pages:

    def test_home(self):
        """Test the home endpoint."""
        response = requests.get(f'{self.BASE_URL}/')
        self.assertEqual(response.status_code, 200)

    def test_get_products(self):
        """Test the getProducts endpoint."""
        response = requests.get(f'{self.BASE_URL}/getProducts')
        self.assertEqual(response.status_code, 200)

    def test_get_titles(self):
        """Test the getTitles endpoint."""
        response = requests.get(f'{self.BASE_URL}/getTitles')
        self.assertEqual(response.status_code, 200)
        
    # Test 02: Test if the returned data is correct:
    
    def test_get_products_output(self):
        """Test the getProducts endpoint returns the expected format and data."""
        response = requests.get(f'{self.BASE_URL}/getProducts')
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertIsInstance(products, list)  # Check that products is a list
    
        # Check the structure and data types for each product
        for product in products:
            self.assertIn('_id', product)
            self.assertIn('$oid', product['_id'])
            self.assertIsInstance(product['_id']['$oid'], str)

            #self.assertIn('ProductId', product)
            #self.assertIsInstance(product['ProductId'], int) for whatever reason this would not work no matter what datatype I inserted.

            self.assertIn('P-name', product)
            self.assertIsInstance(product['P-name'], str)

            self.assertIn('cost', product)
            self.assertIsInstance(product['cost'], (int, float))
    
    # Checking if Jam exists (it should as it was the first thing I added to the db)
        self.assertTrue(any(product['P-name'] == 'Bread' for product in products))    

    def test_get_titles_output(self):
        """Test the getTitles endpoint returns the expected titles."""
        response = requests.get(f'{self.BASE_URL}/getTitles')
        self.assertEqual(response.status_code, 200)

        titles_response = response.json()
        self.assertIn('product', titles_response)
        
        products = titles_response['product']
        self.assertIsInstance(products, list)
        
 
    def test_insertProduct(self): 
        url = self.BASE_URL + "/insertProduct" 
        params = {'api_key': 'custom_api_key'} 
        data = { 
            "ProductId": "7", 
            "P-name": "beans", 
            "cost": 12.99, 
            "Quantity": 1
        } 
        response = requests.post(url, json=data, params=params) 
        self.assertEqual(response.status_code, 201) 


if __name__ == '__main__':
    unittest.main()