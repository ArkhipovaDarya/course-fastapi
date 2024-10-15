from pydantic import BaseModel


# class Item(BaseModel):
#     item: str
#     status: str


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
