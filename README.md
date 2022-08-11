# fastapi-test

## 파이썬 패키지 관리툴 poetry

### 참고

- [poetry 공식사이트](https://python-poetry.org/)
- [파이썬 패키지 관리툴](https://blog.gyus.me/2020/introduce-poetry/)
- [파이썬 의존성 관리자 Poetry 사용기](https://spoqa.github.io/2019/08/09/brand-new-python-dependency-manager-poetry.html)

## poetry 를 사용하는 프로젝트에서 vscode 설정 적용하기

poetry는 virtualenv 환경을 프로젝트 내부가 아닌 홈 디렉토리에 구축하는데 이를 프로젝트 내부로 변경하면 된다. 변경한 이후에 vscode를 재시작하면 알아서 `./.venv/bin/python` 을 인터프리터로 인식해서 원하는대로 동작한다. 수정하는 방법은 다음과 같다.

```bash
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"

# 프로젝트 내부에 venv 새로 설치
poetry install && poetry update
```

마지막으로 vscode를 재시작하고 `Python: Select Interpreter` 로 `.venv/bin/python`을 선택하면 된다.
