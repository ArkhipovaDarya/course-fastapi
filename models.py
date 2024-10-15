from pydantic import BaseModel


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
