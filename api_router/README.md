## Router Test



```shell
$ cd api_router
$ poetry run uvicorn main:app --reload --port 8000

$ http ':8000/users/?skip=0&limit=10'
$ http ':8000/items/?skip=0&limit=10'
```

