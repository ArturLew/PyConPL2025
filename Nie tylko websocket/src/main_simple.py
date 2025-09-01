import os
import json

from typing import AsyncGenerator

import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError, RedisError

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from sse_starlette.sse import EventSourceResponse

SSE_EVENT_NAME = 'push'
STATUS_STREAM_RETRY_TIMEOUT = 2_000

async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        yield redis_client
    finally:
        await redis_client.close()

async def events_generator(request: Request, rc: redis.Redis):
    yield {
        'event': SSE_EVENT_NAME,
        'retry': STATUS_STREAM_RETRY_TIMEOUT,
        'data': json.dumps({'ip': request.client.host, 'message': 'Połączenie'}),
        'id': '-1',
    }

    while True:
        if await request.is_disconnected():
            break

        try:
            resps = await rc.xread({SSE_EVENT_NAME: '$'}, count=10, block=STATUS_STREAM_RETRY_TIMEOUT)

            if not resps:
                continue

            for resp in resps:
                _, messages = resp
                _, data = messages[0]

                yield {
                    'event': SSE_EVENT_NAME,
                    'retry': STATUS_STREAM_RETRY_TIMEOUT,
                    'data': json.dumps(data),
                    'id': '-1'
                }
        except (ConnectionError, TimeoutError, RedisError) as ex:
            break

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/put-one-item')
async def put_one_item(request: Request, rc: redis.Redis = Depends(get_redis_client)) -> None:
    await rc.xadd(SSE_EVENT_NAME, {'task': 'put_one_item', 'ip': request.client.host, 'message': f'PyCon2025 PL'}, maxlen=20, approximate=False)

@app.get('/stream')
async def stream(request: Request, rc: redis.Redis = Depends(get_redis_client)):
    event_generator = events_generator(request, rc)
    return EventSourceResponse(event_generator)
