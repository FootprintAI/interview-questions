from locust import HttpUser, task, between

class HelloWorldUser(HttpUser):
    wait_time = between(0.5, 2.5)

    @task
    def get_world(self):
        self.client.get('/api/')
    
    @task
    def post_world(self):
        self.client.post('/api/')