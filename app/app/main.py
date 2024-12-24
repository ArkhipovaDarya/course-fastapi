import asyncio
import json
import uuid
import time
import os

import fastapi
from fastapi import HTTPException
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError
from pika.exchange_type import ExchangeType
from dotenv import load_dotenv
from clickhouse_driver import Client
from pydantic import BaseModel

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
RABBITMQ_QUEUE = "data_queue"
RABBITMQ_EXCHANGE = "data_exchange"

app = fastapi.FastAPI()

ch_client = Client(host=CLICKHOUSE_HOST)


def create_rabbitmq_connection():
    try:
        connection = BlockingConnection(ConnectionParameters(host=RABBITMQ_HOST)) # Используем host из переменных окружения
        channel = connection.channel()
        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=ExchangeType.direct)
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE)
        return channel, connection
    except AMQPConnectionError as e:
        print(f"rabbitmq connection error: {e}")
        raise HTTPException(status_code=500, detail="failed to connect to rabbitmq")


rabbit_channel, rabbit_connection = create_rabbitmq_connection()


def create_table():
    try:
        ch_client.execute(
            "create table if not exists default.data_table (data String) engine = MergeTree() order by data"
        )
    except Exception as e:
        print(f"table creating error: {e}")


class DataItem(BaseModel):
    data: dict


@app.post("/send")
async def send_data(data: dict):
    try:
        message = json.dumps(data).encode("utf-8")
        rabbit_channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=RABBITMQ_QUEUE,
            body=message,
        )
        return {"info": "data sent"}
    except AMQPConnectionError as e:
        raise HTTPException(status_code=500, detail=f"rabbit connection error: {e}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"invalid json data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to send data")


@app.get("/data")
async def get_data():
    try:
        response = ch_client.execute("select * from data_table")
        form_data = []
        for row in response:
            try:
                form_data.append(json.loads(row[0]))
            except json.JSONDecodeError:
                form_data.append(row[0])
        return form_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to get data")


def data_processing(ch, method, properties, body):
    try:
        data = body.decode("utf-8")
        ch_client.execute(
                f"insert into default.data_table (data) values (toString('{data}'))"
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"data inserted: {data}")
    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        print(f"data processing error: {e}")


def start_consumer():
    global rabbit_channel, rabbit_connection
    while True:
        try:
            rabbit_channel.basic_qos(prefetch_count=1)
            rabbit_channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=data_processing)
            while True:
                rabbit_channel.connection.process_data_events(time_limit=1)
        except AMQPConnectionError as e:
            print(f"rabbitmq connection lost: {e}")
            time.sleep(5)
            try:
                rabbit_channel, rabbit_connection = create_rabbitmq_connection()

            except Exception as e:
                print(f"rabbitmq connection lost: {e}")
                time.sleep(5)


@app.on_event("startup")
async def startup():
    create_table()
    print("starting consumer..")
    asyncio.create_task(asyncio.to_thread(start_consumer))


@app.on_event("shutdown")
async def shutdown():
    print("shutting down consumer..")
    rabbit_channel.close()
    rabbit_connection.close()
