# 01-rate-limit
>Rate limiting is used to protect resources from being over-using or abused by users/bots/applications. It is commonly implemented by social media platforms such as Facebook or Instagram.
## The project components
用Django做應用框架搭配 [django-ratelimit](https://django-ratelimit.readthedocs.io/en/stable/)做速率限制，在資料庫上用Sqlite做每個使用者的header file的紀錄。


## Usage
1. 建立Image，tag加入"v3.3.1"，或者自行至`docker-compose.yml`修改web的image的賦予名稱

```
docker build -t="v3.3.1" .
```
2.載入[locustio/locust](https://hub.docker.com/r/locustio/locust)，Load testing 的工具
```
docker pull locustio/locust
```

3.啟動container
```
docker-compose up --scale worker=4
```
4.開啟網頁，導向 http://localhost:8000/api/  
![image](/image/webpage.png "This is a sample image.")


## Test
使用Postman和撰寫Django Test做基本ratelimit測試，也加入[Locust](https://locust.io/)做Load testing 和 Profiling 評估。  
### Postman
Postman 是常用的api測試工具，我們可以透過Postman簡單的進行Request，也可以透過該工具清楚的看到response的header field。  

Get  
![image](/image/postman_get.png "This is a sample image.")   

Post  
![image](/image/webpage.png "This is a sample image.")  

### Django Test
透過Django Test 可以自訂義test的方法，並觀察1秒內的Request count，超過後顯示"Over Rating"  
```
docker-compose run web python3 manage.py test
```
* 自訂義Django Test 4種測試:  
    1. 在1秒內Request Get 100個請求(不超過rate limit)  
    2. 在1秒內Request Post 1個請求(不超過rate limit)  
    3. 在1秒內Request Get 101個請求(超過rate limit)  
    4. 在1秒內Request Post 2個請求(超過rate limit)  
    
![image](/image/django_test.png "This is a sample image.")

### Locust
> [Locust](https://locust.io/)  
Define user behaviour with Python code, and swarm your system with millions of simultaneous users.  

設定頁面  
![image](/image/locust_index.png "This is a sample image.")  

測試數據  
![image](/image/locust_statistics.png "This is a sample image.") 

錯誤Request內容  
![image](/image/locust_failures.png "This is a sample image.")  


