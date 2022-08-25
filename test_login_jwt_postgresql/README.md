## 로그인 테스트 (JWT Token, ORM with Postrgesql)



### 설치

```shell
$ poetry add python-jose
$ poetry add "pydantic[email]"
$ poetry add "passlib[bcrypt]"
$ poetry add psycopg2-binary
```



### 디렉토리 구조

```shell
.
├── README.md
├── app
│   ├── api
│   ├── core
│   ├── crud
│   ├── db
│   ├── models
│   └── schemas
├── main.py
└── pg
```

pg : postgresql 데이터 보관

app.api : api 파일

app.core : 설정, 디펜던시

app.crud : crud -> db

app.db : db connection manage, init data

app.models : orm code

app.schemas : pydantic 



### 설정

##### postgresql 실행 - 도커이용

```shell
$ docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=1234 -v ~/Project/fastapi-test/test_login_jwt_postgresql/pg:/var/lib/postgresql/data postgres

$ docker ps -a
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                    NAMES
46928484105c   postgres:latest   "docker-entrypoint.s…"   21 seconds ago   Up 20 seconds   0.0.0.0:5432->5432/tcp   postgres
$ docker exec -it postgres /bin/bash
root@46928484105c:/# psql -U postgres
psql (14.2 (Debian 14.2-1.pgdg110+1))
Type "help" for help.

postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
postgres=# CREATE DATABASE app OWNER postgres ENCODING 'utf-8';
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 app       | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(4 rows)
postgres=# \q
root@46928484105c:/# exit
```

##### Secret Key

```shell
$ openssl rand -hex 32
3576b9741008af2f5d1f21672d92f0b38266b2441991b34e5f0ae4e41bb0e75b
```

##### .env 만들기

```bash
SECRET_KEY='3576b9741008af2f5d1f21672d92f0b38266b2441991b34e5f0ae4e41bb0e75b'
HOST='localhost'
PORT=5432

USERNAME='postgres'
PASSWORD='1234'
DATABASE='app'
FIRST_SUPERUSER_EMAIL='jin.yu@vuno.co'
FIRST_SUPERUSER_PASSWORD='$2b$12$X3nAOO/3wqEMzg3VfXUsZ.GuMznpdOVjDYjC/IOWz7M0DokuBDQ8W'
```



### RUN

```shell
$ poetry run uvicorn main:app --reload --port 8000
```

