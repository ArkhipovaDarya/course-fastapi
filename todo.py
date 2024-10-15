from fastapi import APIRouter, Path, HTTPException, status
from models import Todo, TodoItem, TodoItems

todo_router = APIRouter()
todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Successfully added"}


@todo_router.get("/todo", response_model=TodoItems)
async def get_todo() -> dict:
    return {"todo": todo_list}


@todo_router.get("/todo/{todo_id}")
async def get_this_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo does not exist"
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_item: TodoItem, todo_id: int = Path(..., title="The ID of the todo to update")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_item.item
            return {"message": "Successfully updated"}
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo does not exist"
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_this_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {"message": "Successfully deleted"}
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo does not exist"
    )


@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {"message": "Successfully deleted"}
