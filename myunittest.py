import unittest
from fastapi.testclient import TestClient
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_all_products(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        # Add assertions to check the response body and data if needed

    def test_get_product(self):
        product_id = 1
        response = self.client.get(f"/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        # Add assertions to check the response body and data if needed

    def test_create_product(self):
        payload = {
            "name": "Test Product",
            "category": "Test Category",
            "sku": "TEST123",
            "price": 9.99,
            "quantity": 10
        }
        response = self.client.post("/products", json=payload)
        self.assertEqual(response.status_code, 201)
        # Add assertions to check the response body and data if needed

    # Add more test cases for other endpoints and functionalities

if __name__ == '__main__':
    unittest.main()
