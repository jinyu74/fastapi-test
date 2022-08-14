# fastapi-test

FastAPI 는 모던파이썬(3.6+)문법을 사용하므로 3.6 이상이 설치되어야 한다.



## 환경설정

```bash
$ mkdir fastapi-test && cd fastapi-test
# 설정진행
$ poetry init

# 설치..
$ poetry add fastapi
$ poetry add "uvicorn[standard]"
# 설치된 패키지 확인
$ poetry show
# 설치된 패키지 삭제 poetry remove [패키지명]
```



##### 기본페이지 작성

`main.py`

```py
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
  return {"Hello": "World"}
```

##### 실행

**[Uvicorn](https://www.uvicorn.org/)**? uvloop 및 httptools를 사용하는 ASGI web server 이다.

*ASGI(Asynchronous Server Gateway Interface)는 비동기 Python 웹 서버입니다.*

**uvloop**는 **asyncio**를 대체하기 위해 만들어졌습니다. Uvloop는 **Cython**으로 작성되었으며 **libuv** 위에 구축되었습니다. (여기서**libuv**는 nodejs에서 사용하는 고성능 다중 플랫폼 비동기 I / O 라이브러리입니다.)

실제 성능상에서 nodejs, gevent 및 기타 Python 비동기 프레임 워크보다 2배 이상 빠릅니다. 성능상으로만 본다면, uvloop 기반 asyncio의 성능은 **Go 프로그램의 성능에 가깝습니다.**

> Asyncio는 Python 표준 라이브러리와 함께 제공되는 비동기 I/O 프레임 워크입니다. Asyncio는 async / await 구문을 사용하여 비동기(Asynchronous) 코드를 작성하는 라이브러리입니다. Asyncio는 대규모 I / O 처리 및 복잡하게 설계된 서버 구조에 적합합니다. 대표적인 I / O에서의 병목의 예시는, 웹 서버와 같은 애플리케이션에서 찾아볼 수 있습니다. CPU 연산 시간 대비 DB나 API와 연동 과정에서 발생하는 대기 시간이 훨씬 긴 경우가 빈번합니다. 비동기 프로그래밍은 이러한 대기 시간을 낭비하지 않고 그 시간 CPU가 다른 처리를 할 수 있도록 하는데 이를 흔히 **non-blocking**하다고 합니다. 반대로 동기적 블로킹을 통해 CPU가 다른 업무를 처리 하지 못하면 이를 blocking 되있다고 말합니다.



```bash
$ poetry run uvicorn main:app --reload --port 8000
```

poetry로 패키지 관리를 하는경우 poetry run으로 실행하게 된다. 

main:app => 파이썬파일명:FastAPI()의 app을 가리킨다.

reload 는 파일에 변화가 생길때 재시작을 해주겠다는 의미이다.

port 설정을 안하면 기본 8000으로 서빙된다.



눈여겨볼만한 부분

```bash
$ poetry show
..
pydantic          1.9.1  Data validation and settings management using python type hints
..
starlette         0.19.1 The little ASGI library that shines.
```

[**starlette**](https://www.starlette.io/)는 FastAPI가 사용하는 프레임워크로 starlette의 랩퍼인샘이다..

[**pydantic**](https://pydantic-docs.helpmanual.io/)은 파이썬 타입 어노테이션 문법에 근거하여 데이터 검증을 해주는 라이브러리로 marshimallow와 비슷하다. runtime에서 type를 강제하고 type의 유효성 체크와 에러를 발생시킨다.



## FastAPI 기초

#### 경로매개변수

path parameters는 url 경로에 들어가는 변수를 의히마한다

http://localhost:8000/users/123 과 같은 경우 123을 변수로 받는다. url path는 실질적으로 문자로 인식하기 때문에 타입을 지정해주면 좋다.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int):
  return {"user_id": user_id}
```

간단하게 테스트를 위해 [**HTTPie**](https://httpie.io/)를 이용해 콘솔창에서 바로 테스트 해본다.

```bash
$ brew install httpie

$ http :8000/users/123
HTTP/1.1 200 OK
content-length: 15
content-type: application/json
date: Fri, 12 Aug 2022 01:48:12 GMT
server: uvicorn

{
    "user_id": 123
}

# 타입을 int로 지정후 부동소수형 매개변수를 전달하는 경우..FastAPI가 적절히 응답해준다.
$ http :8000/users/123.3
HTTP/1.1 422 Unprocessable Entity
content-length: 104
content-type: application/json
date: Fri, 12 Aug 2022 01:49:34 GMT
server: uvicorn

{
    "detail": [
        {
            "loc": [
                "path",
                "user_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

유의사항으로 FastAPI는 앤드포인트의 순서에 따라 수행하기 때문에 아래코드 처럼 작성하는 경우

```python
@app.get("/users/{user_id}")
...

@app.get("/users/me")
```

아래와 같은 결과를 얻게 된다. 

```bash
$ http :8000/users/me
HTTP/1.1 422 Unprocessable Entity
content-length: 104
content-type: application/json
date: Fri, 12 Aug 2022 01:53:50 GMT
server: uvicorn

{
    "detail": [
        {
            "loc": [
                "path",
                "user_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

`/users/{user_id}`는 매개변수 `user_id`의 값을 `me`라고 생각하여 `/users/me`도 연결하기 때문이다. 이를 해결하려면 `/users/me`를 먼저 선언해야 한다.









#### 쿼리매개변수



#### 요청본문



#### 응답모델



#### 데이터검증



#### 헤더,쿠키 매개변수



## FastAPI 실무

#### RDB연동



#### 파일처리



#### 에러처리



#### 의존성주입



#### 인증



32바이트 랜덤문자 생성

```bash
$ openssl rand -hex 32
# 또는 파이썬으로 할 수 있습니다
$ python -c "import secrets;print(secrets.token_hex(32))"
```

bcrypt로 비밀번호 생성하기

hashpw 함수에 넣기 전에 비밀번호를 **encoding** 해서 **type을 byte로** 바꿔줘야 한다.

```python
>>> import bcrypt
>>> password = "password".encode()
>>> # 또는
>>> password = b"password"
>>> hashed = bcrypt.hashpw(password, bcrypt.gensalt())
>>> type(hashed) # output : <class 'bytes'>
```

password를 확인할 때에는 str값으로 받아 매칭하기 때문에, 비밀번호를 데이터베이스에 저장할 때 decoding을 해줘야 한다.

```python
>>> password = hashed.decode()
>>> type(password) # output : <class 'str'>
```









#### 백그라운드작업



#### 미들웨어









## 부록

### 참고

- [poetry 공식사이트](https://python-poetry.org/)
- [파이썬 패키지 관리툴](https://blog.gyus.me/2020/introduce-poetry/)
- [파이썬 의존성 관리자 Poetry 사용기](https://spoqa.github.io/2019/08/09/brand-new-python-dependency-manager-poetry.html)

### poetry 를 사용하는 프로젝트에서 vscode 설정 적용하기

poetry는 virtualenv 환경을 프로젝트 내부가 아닌 홈 디렉토리에 구축하는데 이를 프로젝트 내부로 변경하면 된다. 변경한 이후에 vscode를 재시작하면 알아서 `./.venv/bin/python` 을 인터프리터로 인식해서 원하는대로 동작한다. 수정하는 방법은 다음과 같다.

```bash
$ poetry config virtualenvs.in-project true
$ poetry config virtualenvs.path "./.venv"

# 프로젝트 내부에 venv 새로 설치
$ poetry install && poetry update
```

마지막으로 vscode를 재시작하고 `Python: Select Interpreter` 로 `.venv/bin/python`을 선택하면 된다.
