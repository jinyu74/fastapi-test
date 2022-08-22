# FastAPI

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



### 경로매개변수

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





### 쿼리매개변수

```bash
$ http ':8000/users?limit=100'
```

**limit=100**을 받기 위해서는 아래와 같다

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users(limit: int = 100):
  return {"limit": limit}
```

**bool**형인 경우 `true`, `True`, `1`, `TRUE`, `on`, `yes` 모두 가능

```bash
$ http ':8000/users/1234/items/apple?q=&short=true'
```

```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

```

필수 쿼리 매개변수를 전달 하지 않는 경우에는 오류가 발생한다. 이에 기본값을 설정하거나 필수 쿼리 매개변수를 전달해야 한다.



**열거형** 데이터 지정

```python
from enum import Enum

from fastapi import FastAPI

app = FastAPI()

class UserLevel(str, Enum):
    a = "a"
    b = "b"
    c = "c"


@app.get("/users")
def get_users(grade: UserLevel = UserLevel.a):  # 추가: UserLevel 기본값
    return {"grade": grade}
```



### 요청본문

pydantic을 이용하여 쉽게 구현이 가능

pydantic 에는 `HttpUrl` 은 url 형식을 검증해준다. `EmailStr`도 있다. 이메일 주소를 검증해 주는것이다. 설치 필요

```python
from typing import Optional, List  # 추가: List

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


# 추가: Item 클래스
class Item(BaseModel):
    name: str
    price: float
    amount: int = 0


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None # HttpUrl | None = None 으로 표현 가능 3.10^
    inventory: List[Item] = []  # 추가: inventory


@app.post("/users")
def create_user(user: User):
    return user


# 추가: get_user()
@app.get("/users/me")
def get_user():
    fake_user = User(
        name="Nathan",
        password="1234",
        inventory=[
            Item(name="전설 무기", price=1_000_000),
            Item(name="전설 방어구", price=900_000),
        ]
    )
    return fake_user
```

```bash
$ http :8000/users/me
HTTP/1.1 200 OK
content-length: 181
content-type: application/json
date: Thu, 15 Apr 2021 13:06:11 GMT
server: uvicorn

{
    "avatar_url": null,
    "inventory": [
        {
            "amount": 0,
            "name": "전설 무기",
            "price": 1000000.0
        },
        {
            "amount": 0,
            "name": "전설 방어구",
            "price": 900000.0
        }
    ],
    "name": "FastCampus",
    "password": "1234"
}
```



중첩모델을 표현하기 힘드므로 스웨거 이용이 편함.

```bash
$ http POST :8000/users name=Nathan password=1q2w3e4r inventory:='[{"name": "어떤 무기", "price": 10.0, "amount": 99}]'
HTTP/1.1 200 OK
content-length: 125
content-type: application/json
date: Thu, 15 Apr 2021 13:15:52 GMT
server: uvicorn

{
    "avatar_url": null,
    "inventory": [
        {
            "amount": 99,
            "name": "어떤 무기",
            "price": 10.0
        }
    ],
    "name": "FastCampus",
    "password": "1q2w3e4r"
}
```







### 응답모델

데코레이터 메소드의 매개변수로 `response_model` 을 추가하고 `GetUser`를 할당하여 요청 모델과 응답모델을 단순하게 클래스로 나누어 분리 할 수 있다. 응답모델을 사용하면 스웨거를 통해 어떻게 오는지 미리 확인할 수 있어 결과를 검증하는데 도움이 된다.

```python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class CreateUser(BaseModel):
    name: str
    password: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class GetUser(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


@app.post("/users", response_model=GetUser)  # 응답 모델
def create_user(user: CreateUser):  # 요청 모델
    return user
```



모델이 명확해지지 않아 **추천되지 않지만** 아래와 같은 매개변수가 있다.

- response_model_include
- response_model_exclude
- response_model_exclude_unset

```python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str = "fastapi"
    password: str
    avatar_url: HttpUrl = None


@app.post(
    "/include",
    response_model=User,
    response_model_include={"name", "avatar_url"},  # Set 타입. List도 괜찮습니다.
)
def get_user_with_include(user: User):
    return user


@app.post(
    "/exclude",
    response_model=User,
    response_model_exclude={"password"},
)
def get_user_with_exclude(user: User):
    return user


@app.post(
    "/unset",
    response_model=User,
    response_model_exclude_unset=True,
)
def get_user_with_exclude_unset(user: User):
    return user
```



**응답코드** : [HTTP Status](https://developer.mozilla.org/ko/docs/Web/HTTP/Status)

`status` 를 추가해서 응답코드를 지정할 수 있다.

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)  # 추가: status_code
def create_user(user: CreateUser):
    return user
```





### 데이터검증

FastAPI는 데이터 검증을 위해 방어코드를 작성하는것을 알아서 해준다. 타입 검증의 필수인지 아닌지만 단순히 봤지만 세밀한 제어가 가능하다.

**Path**, **Query**는 `Params` 클래스의 서브 클래스를 반환하는 함수이다. `Path()`, `Query()` 함수를 이용하면 매개변수를 명시적으로 정의할 수 있고, 다양한 옵션을 추가할 수 있다.

```python
from typing import List

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, parse_obj_as

app = FastAPI()

inventory = (
    {
        "id": 1,
        "user_id": 1,
        "name": "레전드포션",
        "price": 2500.0,
        "amount": 100,
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "포션",
        "price": 300.0,
        "amount": 50,
    },
)


class Item(BaseModel):
    name: str
    price: float
    amount: int = 0


@app.get("/users/{user_id}/inventory", response_model=List[Item])
def get_item(
    user_id: int = Path(..., gt=0, title="사용자 id", description="DB의 user.id"),
    name: str = Query(None, min_length=1, max_length=2, title="아이템 이름"),
):
    user_items = []
    for item in inventory:
        if item["user_id"] == user_id:
            user_items.append(item)

    response = []
    for item in user_items:
        if name is None:
            response = user_items
            break
        if item["name"] == name:
            response.append(item)

    return response
```

```shell
$ http ':8000/users/1/inventory?name=포션'
```



영어뿐만 아니라 한글도 글자 갯수를 정확하게 측정한다.

- `gt`, `ge`, `lt`, `le`: 숫자
- `min_length`, `max_length`: `str`
- `min_items`, `max_items`: 컬렉션(e.g. `List`, `Set`)

뿐만 아니라 `regex` 옵션으로 정규표현식 검증도 가능



**요청 본문**은 `pydantic`의 클래스로 만들어서 아래와 같이 정의 할수 있다.

```python
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, title="이름")
    price: float = Field(None, ge=0)
    amount: int = Field(
        default=1,
        gt=0,
        le=100,
        title="수량",
        description="아이템 갯수. 1~100 개 까지 소지 가능",
    )


@app.post("/users/{user_id}/item")
def create_item(item: Item):
    return item
```

간단한 모델을 받을 때는 `Body` 클래스를 이용하는 방법도 있다. 사용법은 `Query`, `Path` 와 형태가 같다.





### 헤더,쿠키 매개변수

#### 🍪 쿠키 가져오기

```python
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/cookie")
def get_cookies(ga: str = Cookie(None)):
    return {"ga": ga}
```

쿠키는 사이트에서 정보 수집을 하는 프로그램들이 자주 사용한다.

```bash
$ http :8000/cookie Cookie:ga=GA12.3.4
```

HTTPie에서 쿠키는 `Cookie:<key>=<value>;<key>=<value>`와 같이 작성한다. `;`은 구분자이다.

#### 헤더 가져오기

HTTP 헤더는 종류도 많고 커스텀 헤더도 많이 사용한다.

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/header")
def get_headers(x_token: str = Header(None, title="토큰")):
    return {"X-Token": x_token}
```

헤더에 `X-` 접두어는 사용자 정의 헤더라는 것을 의미한다. 반드시 이렇게 할 필요는 없지만, 표준 헤더와 구분짓기 위해 사용한다. 사실.. 이 [정책은 폐기](https://tools.ietf.org/html/rfc6648) 되었지만, 여전히 다들 이 관례를 따르고 있다.

눈 여겨 볼 점은, 파이썬에서 `-`을 변수명으로 허락하지 않기 떄문에, 언더스코어(`_`)를 대신 사용해야 하고 대소문자 구분을 하지 않는다. 실제로는 아래와 같이 테스트하면 정상 작동한다.

```bash
http :8000/header X-Token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Imppbi55dUB2dW5vLmNvIiwiZmlyc3RfbmFtZSI6Ill1IiwibGFzdF9uYW1lIjoiSmluIiwibWlkZGxlX25hbWUiOiJKb2VsIiwiZ2VuZGVyIjoibWFsZSIsInJvbGVzIjpbImFkbWluIl0sInBhc3N3b3JkIjoiJDJiJDEyJDFSVHdFYy5tNUlxQTIydU0zaGswc2VnUkpHekROSC9BWHJHL3RrV1ljc095MVIxME94bXJLIiwiZXhwIjoxNjYxMTQwODAwfQ.zi7Rqk7CIVrFQh3AzTIp9ErldUecgAykWSV5u-jgUQI
```

추가로 `Header`는 다른 클래스와 다르게 `convert_underscores` 옵션을 갖는데 `False`를 줄 경우 하이픈을 언더스코어로 변환하지 않는다.  `X-token`이 아니라 `X_Token`이라는 헤더를 위해 존재하는 옵션이지만 애초에 언더스코어를 사용하는 건 관례를 벗어나므로 웬만해서는 하지 않아야 한다.





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
