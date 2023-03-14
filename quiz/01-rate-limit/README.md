#### Rate limiting

Rate limiting is used to protect resources from being over-using or abused by users/bots/applications. It is commonly implemented by social media platforms such as Facebook or Instagram.

Header fields and status codes from the response of a rate-limited server could tell you more information about how it is going to limit your requests. 

| header field | explaination |
|-------------|--------------|
|  X-RateLimit-Limit           | The number of requests allowed during a fixed time window.             |
|  X-Rate-Limit-Remaining           |    The number of remaining requests allowed in the current time window.          |
|  X-Rate-Limit-Reset           |  at the time when the rate-limit requests are reset.  UTC epoch time (in seconds).          |
| Retry-At |  the second before the window resets and requests will be accepted. UTC epoch time (in seconds). |


For example, the following messages would tell the client that you sent too many requests to the server side, and now you are temporarily blocked for an hour, you can try later by then.

```
HTTP/1.1 429 Too Many Requests
Content-Type: text/html
Retry-After: 3600
```


#### Requirement

Please implements a service that provides one endpoint (e.g. /foo) with two different methods (i.e. GET / POST) with different rate limit configuration. Let's say we want 1 request per IP per second for the POST method, but 100 requests per IP per second for the GET method, which is a fast-read-slow-write scenario.

The request should be counted as one when they first hit into the API, even if the API is running a long job and has not returned yet.

Besides that, the server should be survived up-and-down scenarios, which is a common scenario when your application is running in the production environment. The rate limit state must be kept during the server is up and down.

Each endpoint should follow the above-mentioned headers and response body to better explain the situation to the clients.


#### Environment

Please make sure you can follow the following rules:

1. (basic) There is NO preferred programming language, pick one you are most comfortable with.
2. (must) Provide a build-able Dockerfile to run your application
3. (must) Provide test cases for your application
4. (bonus) Concurrently test your application
5.  (bonus) Benchmark your application