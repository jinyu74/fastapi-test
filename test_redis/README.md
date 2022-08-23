## REDIS 테스트



```shell
# 도커로 기본 Redis 띄우기
$ docker run -d --name redis -p 6379:6379 --network redis-net redis 
# 볼륨 설정하기 
$ docker run --name redis -p 6379:6379 --network redis-net -v ~/redis/volume -d redis:latest redis-server --appendonly yes
# Redis Cli 접속
$ docker exec -it redis redis-cli
# FastAPI Run
$ poetry run uvicorn main:app --reload --port 8000
$ http :8000
HTTP/1.1 200 OK
content-length: 25
content-type: application/json
date: Tue, 23 Aug 2022 06:46:45 GMT
server: uvicorn

{
    "message": "Hello World"
}
```



```shell
$ docker exec -it redis redis-cli
127.0.0.1:6379> get message
"{\"message\": \"Hello World\"}"
```



