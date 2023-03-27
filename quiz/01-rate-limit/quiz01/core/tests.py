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
        print('-----------Get not over-----------')
        resp = self.c.post('/reset/',{'group':'get', 'key':'ip', 'rate':'100/s', 'method':'GET'})
        t0 = time.time()
        for i in range(1,101):
            resp = self.c.get('/api/')
            print(resp.content)
        print('execution time: '+str(time.time()-t0))
        self.assertEqual(resp.status_code, 200)
        
    # Over rate limiting get test 
    # will be get 429 status
    def test_get_over100(self):
        print('-----------Get over-----------')
        self.c.post('/reset/',{'group':'get', 'key':'ip', 'rate':'100/s', 'method':'GET'})
        t0 = time.time()
        for i in range(1,102):
            resp = self.c.get('/api/')
            print(resp.content)
        print('execution time: '+str(time.time()-t0))
        self.assertEqual(resp.status_code, 429)

    # Unover rate limiting post test 
    # will be get 200 status
    def test_post_not_over(self):
        print('-----------Post not over-----------')
        self.c.post('/reset/',{'group':'post', 'key':'ip', 'rate':'1/s', 'method':'POST'})
        t0 = time.time()
        resp = self.c.post('/api/')
        print(resp.content)
        print('execution time: '+str(time.time()-t0))
        self.assertEqual(resp.status_code, 200)

    # # Over rate limiting post test 
    # # # will be get 429 status
    def test_post_over1(self):
        print('-----------Post over-----------')
        resp = self.c.post('/reset/',{'group':'post', 'key':'ip', 'rate':'1/s', 'method':'POST'})
        t0 = time.time()
        resp = self.c.post('/api/')
        print(resp.content)
        resp = self.c.post('/api/')
        print(resp.content)
        print('execution time: '+str(time.time()-t0))
        self.assertEqual(resp.status_code, 429)    

