from django.test import TestCase
from django.test import client
import time
# Create your tests here.

class APITestCase(TestCase):

    def setUp(self):
        self.c = client.Client()

    # # Unover rate limiting get test 
    # # will be get 200 status
    def test_get_not_over(self):
        print('-----------Get not over-----------')
        
        # If the execution time is greater than 1 second, 
        # we must retest until it is less than 1 second or has been executed 5 times  
        for i in range(1,5):
            #reset api limit
            resp = self.c.post('/reset/',{'group':'get', 'key':'ip', 'rate':'100/s', 'method':'GET'}) 
            t0 = int(time.time())
            #number of request
            for j in range(1,101):
                resp = self.c.get('/api/') #request api

                # get diff header file by status code
                if(resp.status_code == 200):
                    print('[X-RateLimit-Limit]: '+ resp['X-RateLimit-Limit'] 
                        + ' [X-RateLimit-Remaining]: '+ resp['X-RateLimit-Remaining'] 
                        + ' [X-RateLimit-Reset]: '+ resp['X-RateLimit-Reset'])
                elif(resp.status_code == 429):
                    print('[Retry-At]: '+ resp['Retry-At'] )
            t1 = int(time.time())

            # if execution time < 1, don't do again
            if((t1-t0) <1):
                break
        print('execution time: '+str(t1-t0))

        if((t1-t0) >1):
            self.assertEqual(0, 1) #we can't get it for less than 1s
        else:
            self.assertEqual(resp.status_code, 200)
        
    # # Over rate limiting get test 
    # # will be get 429 status
    def test_get_over100(self):
        print('-----------Get over-----------')
        

        # If the execution time is greater than 1 second, 
        # we must retest until it is less than 1 second or has been executed 5 times 
        for i in range(1,5):
            #reset api limit
            self.c.post('/reset/',{'group':'get', 'key':'ip', 'rate':'100/s', 'method':'GET'})
            t0 = int(time.time())

            #number of request
            for j in range(1,102):
                resp = self.c.get('/api/') #request api

                # get diff header file by status code
                if(resp.status_code == 200):
                    print('[X-RateLimit-Limit]: '+ resp['X-RateLimit-Limit'] 
                        + ' [X-RateLimit-Remaining]: '+ resp['X-RateLimit-Remaining'] 
                        + ' [X-RateLimit-Reset]: '+ resp['X-RateLimit-Reset'])
                elif(resp.status_code == 429):
                    print('[Retry-At]: '+ resp['Retry-At'] )
            t1 = int(time.time())

            # if execution time < 1, don't do again
            if((t1-t0) <1):
                break

        print('execution time: '+str(t1-t0))
        if((t1-t0) >1):
            self.assertEqual(0, 1) #can't done for less than 1s
        else:
            self.assertEqual(resp.status_code, 429) 


    # # Unover rate limiting post test 
    # # will be get 200 status
    def test_post_not_over(self):
        print('-----------Post not over-----------')
        for i in range(1,5):
            self.c.post('/reset/',{'group':'post', 'key':'ip', 'rate':'1/s', 'method':'POST'})
            t0 = int(time.time())
            resp = self.c.post('/api/') #request api

            # get diff header file by status code
            if(resp.status_code == 200):
                print('[X-RateLimit-Limit]: '+ resp['X-RateLimit-Limit'] 
                    + ' [X-RateLimit-Remaining]: '+ resp['X-RateLimit-Remaining'] 
                    + ' [X-RateLimit-Reset]: '+ resp['X-RateLimit-Reset'])
            elif(resp.status_code == 429):
                print('[Retry-At]: '+ resp['Retry-At'] )
            t1 = int(time.time())

            # if execution time < 1, don't do again
            if((t1-t0) <1):
                break

        print('execution time: '+str(t1-t0))
        if((t1-t0) >1):
            self.assertEqual(0, 1) #can't done for less than 1s
        else:
            self.assertEqual(resp.status_code, 200) 

    # # Over rate limiting post test 
    # # will be get 429 status
    def test_post_over1(self):
        print('-----------Post over-----------')
        for i in range(1,5):
            resp = self.c.post('/reset/',{'group':'post', 'key':'ip', 'rate':'1/s', 'method':'POST'})
            t0 = int(time.time())
            resp = self.c.post('/api/') #request api

            # get diff header file by status code
            if(resp.status_code == 200):
                print('[X-RateLimit-Limit]: '+ resp['X-RateLimit-Limit'] 
                    + ' [X-RateLimit-Remaining]: '+ resp['X-RateLimit-Remaining'] 
                    + ' [X-RateLimit-Reset]: '+ resp['X-RateLimit-Reset'])
            elif(resp.status_code == 429):
                print('[Retry-At]: '+ resp['Retry-At'] )
            resp = self.c.post('/api/')
            if(resp.status_code == 200):
                print('[X-RateLimit-Limit]: '+ resp['X-RateLimit-Limit'] 
                    + ' [X-RateLimit-Remaining]: '+ resp['X-RateLimit-Remaining'] 
                    + ' [X-RateLimit-Reset]: '+ resp['X-RateLimit-Reset'])
            elif(resp.status_code == 429):
                print('[Retry-At]: '+ resp['Retry-At'] )

            t1 = int(time.time())

            # if execution time < 1, don't do again
            if((t1-t0) <1):
                break

        print('execution time: '+str(t1-t0))
        if((t1-t0) >1):
            self.assertEqual(0, 1) #can't done for less than 1s
        else:
            self.assertEqual(resp.status_code, 429)    

