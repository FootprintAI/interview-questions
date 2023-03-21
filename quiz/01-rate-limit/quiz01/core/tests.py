from django.test import TestCase
from django.test import client
import time
# Create your tests here.

class APITestCase(TestCase):

    def setUp(self):
        self.c = client.Client()
    
    # Unover rate limiting get test 
    # will be get 200 status
    def test_get_unover(self):
        time.sleep(1)
        for i in range(1,101):
            resp = self.c.get('/api/')
        self.assertEqual(resp.status_code, 200)
    

    # Unover rate limiting post test 
    # will be get 200 status
    def test_post_unover(self):
        time.sleep(1)
        resp = self.c.post('/api/')
        self.assertEqual(resp.status_code, 200)

    # Over rate limiting get test 
    # will be get 429 status
    
    def test_get_over100(self):
        time.sleep(1)
        for i in range(1,102):
            resp = self.c.get('/api/')
        self.assertEqual(resp.status_code, 429)

    # # Over rate limiting post test 
    # # # will be get 429 status
    def test_post_over1(self):
        time.sleep(1)
        resp = self.c.post('/api/')
        resp = self.c.post('/api/')
        self.assertEqual(resp.status_code, 429)    

