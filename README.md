# pythonanywhere搭建数据存储服务

+ 为腾讯云函数提供数据储存api

+ 存储数据接口
```
resp = requests.post(
    url="https://utf8.pythonanywhere.com/store/",
    data={
        "key": "xxx", 
        "value": "xxx"
    },
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
)
resp.encoding = 'utf8'
print(resp.json())
```
+ 读取数据接口
```
resp = requests.get(
    url="https://utf8.pythonanywhere.com/store/",
    params={
        "key": "xxx"
    },
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
)
resp.encoding = 'utf8'
print(resp.json())
```

+ 计划任务自动延期pythtonanywhere web应用程序、计划任务停运时间
