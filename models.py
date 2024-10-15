from enum import Enum

from pydantic import BaseModel, Field, PositiveFloat, field_validator


class Todo(BaseModel):
    id: int
    item: str

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "id": 1,
                    "item": "Example schema",
                }
            ]
        }
    }


class TodoItem(BaseModel):
    item: str

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "item": "Example item",
                }
            ]
        }
    }


class TodoItems(BaseModel):
    todos: list[TodoItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "todos": [
                    {"item": "Example item 1"},
                    {"item": "Example item 2"},
                ]
            }
        }
    }


# task 1
class User(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "user": [
                    {
                        "id": 1,
                        "name": "<NAME>",
                        "email": "<EMAIL>"
                    }
                ]
            }
        }
    }


# task 2
class Product(BaseModel):
    name: str
    price: PositiveFloat
    in_stock: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "user": [
                    {
                        "name": "<NAME>",
                        "price": 100,
                        "in_stock": False
                    }
                ]
            }
        }
    }


# task 3
class Products(BaseModel):
    products: list[Product]

    model_config = {
        "json_schema_extra": {
            "example": {
                "products": [
                    {
                        "product": {
                            "name": "Example product 1",
                            "price": 100,
                            "in_stock": False
                        }
                    },
                    {
                        "product": {
                            "name": "Example product 2",
                            "price": 200,
                            "in_stock": True
                        }
                    }
                ]
            }
        }
    }


class Zakaz(BaseModel):
    user: User
    products: Products


# task 4
class Topic(BaseModel):
    title: str
    content: str
    published: bool = False


# task 5
class Person(BaseModel):
    first_name: str = Field(..., alias="first")
    last_name: str = Field(..., alias="last")


# task 6
class Profile(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, p: str) -> str:
        if not any(char.isdigit() for char in p):
            raise ValueError('Password must contain at least 1 digit.')
        if not any(char.isupper() for char in p):
            raise ValueError('Password must contain at least 1 uppercase character.')
        return p


# task 7
class PersonInfo(BaseModel):
    first_name: str
    last_name: str
    age: int


# person = PersonInfo(...)
# person_dict = person.dict(exclude={'age'})


# task 8
class Address(BaseModel):
    city: str
    street: str


class Resident(BaseModel):
    username: str
    address: Address


# resident = Resident(...)
# resident_dict = resident.dict(exclude={'address':{'city'}})

# task 9
class Status(str, Enum):
    pending = 'Pending'
    in_progress = 'In progress'
    completed = 'Completed'


class Task(BaseModel):
    title: str
    status: Status


# task 10
class UserGroup(BaseModel):
    users: list[User]

    @field_validator('users')
    def check_users(scls, u):
        if len(u) == 0:
            raise ValueError('Users must not be empty.')
        return u


# task 11
class Order(BaseModel):
    order_id: int
    customer_name: str
    items: list[str]
    total_amount: float
