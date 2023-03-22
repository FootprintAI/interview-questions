from django.test import TestCase
from django.test import client
import time
# Create your tests here.

class APITestCase(TestCase):

    def setUp(self):
        self.c = client.Client()
    
    # Unover rate limiting get test 
    # will be get 200 status
    def test_get_not_over(self):
        time.sleep(2)
        print('-----------Get not over-----------')
        for i in range(1,101):
            resp = self.c.get('/api/')
        self.assertEqual(resp.status_code, 200)
    

    # Unover rate limiting post test 
    # will be get 200 status
    def test_post_not_over(self):
        time.sleep(1)
        print('-----------Post not over-----------')
        resp = self.c.post('/api/')
        self.assertEqual(resp.status_code, 200)

    # Over rate limiting get test 
    # will be get 429 status
    
    def test_get_over100(self):
        time.sleep(2)
        print('-----------Get over-----------')
        for i in range(1,102):
            resp = self.c.get('/api/')
        self.assertEqual(resp.status_code, 429)

    # # Over rate limiting post test 
    # # # will be get 429 status
    def test_post_over1(self):
        time.sleep(1)
        print('-----------Post over-----------')
        resp = self.c.post('/api/')
        resp = self.c.post('/api/')
        self.assertEqual(resp.status_code, 429)    

