# from fastapi import FastAPI
#
# app  = FastAPI()
#
#
# @app.get("/")
# async def welcome():
#     return {'message': 'Главная страница'}
#
#
# @app.get('/user/admin')
# async def admin():
#     return {'message': 'Вы вошли как администратор'}
#
#
# @app.get('/user/{user_id}')
# async def user(user_id):
#     return {'message': f'Вы вошли как пользователь №{user_id}'}
#
#
# @app.get('/user')
# async def user_info(username, age):
#     return f'Информация о пользователе, Имя: {username}, Возраст: {age}'

#
# from fastapi import FastAPI, Path
# from typing import Annotated
#
# app = FastAPI()
#
#
# @app.get('/')
# async def welcome() -> str:
#     return (f'Главная страница')
#
#
# @app.get('/user/admin')
# async def administrator() -> str:
#     return (f'Вы вошли как администратор')
#
#
# @app.get('/user/{user_id}')
# async def user_number(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]):
#     return (f'Вы вошли как пользователь № {user_id}')
#
#
# @app.get('/user/{username}/{age}')
# async def user_info(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
#                     age: Annotated[int, Path(ge=18, le=120, description='Enter age')]):
#     return (f'Информация о пользователе. Имя: {username}, Возраст: {age}')


#
# from fastapi import FastAPI, Path
# from typing import Annotated
#
#
# app = FastAPI()
#
# users = {'1': 'Имя: Example, возраст: 18'}
#
# @app.get('/users')
# async def get_users() -> dict:
#     return users
#
# @app.post('/user/{username}/{age}')
# async def create_user(username: Annotated[str, Path(min_length=3, max_length=15, description='Введите Ваше имя', example=' Сергей')]
#                       , age: int) -> str:
#     current_index = str(int(max(users, key=int)) + 1)
#     users[current_index] = username, age
#     return f'Пользователь {current_index} зарегистрирован!'
#
# @app.put('/user/{user_id}/{username}/{age}')
# async def update_user(user_id: str = Path(ge=1, le=100, description='Введите возраст', example= '1')
#                       , username: str =Path(min_length=3, max_length=20, description=' Введите Ваше имя', example= 'Сергей')
#                       , age: int = 30) -> str:
#     users[user_id] = user_id, username, age
#     return f'Информация о пользователе id# {user_id} обновлена'
#
# @app.delete('/user/{user_id}')
# async def delite_user(user_id: str) -> str:
#     users.pop(user_id)
#     return f'Пользователь {user_id} удалён'





from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="Templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, user_id: int) -> HTMLResponse:
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})

@app.post("/user/{user_name}/{age}", response_model=str)
async def create_user(user: User, user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="OlegV")],
        age: int = Path(ge=18, le=120, description="Enter age", example=55)) -> str:
    if users:
        current_index = max(user.id for user in users) + 1
    else:
        current_index = 1
    user.id = current_index
    user.username = user_name
    user.age = age
    users.append(user)
    return f"User {current_index} is registered"

@app.put("/user/{user_id}/{user_name}/{age}", response_model=str)
async def update_user(user: User, user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="OlegV")],
        age: int = Path(ge=18, le=120, description="Enter age", example=55),
        user_id: int = Path(ge=0)) -> str:
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = user_name
            existing_user.age = age
            return f"The user {user_id} is updated."
    raise HTTPException(status_code=404, detail="Пользователь не найден.")

@app.delete("/user/{user_id}", response_model=str)
async def delete_user(user_id: int = Path(ge=0)) -> str:
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users.pop(index)
            return f"Пользователь с ID {user_id} удален."
    raise HTTPException(status_code=404, detail="Пользователь не найден.")


