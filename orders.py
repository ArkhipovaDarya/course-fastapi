from fastapi import APIRouter, HTTPException, status
from models import Order

order_router = APIRouter()
order_list = {}


@order_router.post('/orders', response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    order_list[order.order_id] = order
    return order


@order_router.get('/orders/{order_id}', response_model=Order, status_code=status.HTTP_200_OK)
async def get_order(order_id: int):
    order = order_list.get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order ID not found'
        )
    return order


@order_router.patch('/orders/{order_id}', response_model=Order, status_code=status.HTTP_200_OK)
async def update_order(order_id: int, new_order: Order):
    if order_id not in order_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order ID not found"
        )
    order_list[order_id].update(new_order)
    return {"message": "Order updated"}


@order_router.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int):
    if order_id not in order_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order ID not found"
        )
    del order_list[order_id]
    return {"message": "Order deleted"}
