import os
import json
import random
import asyncio

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

def jitter_timeout_sec(timeout: float, delta_range: float = 0.5) -> int:
    return int(timeout + random.uniform(-delta_range, delta_range))

async def events_generator(request: Request, rc: redis.Redis, lastEventId: str = '$'):
    try:
        yield {
            'event': SSE_EVENT_NAME,
            'retry': jitter_timeout_sec(STATUS_STREAM_RETRY_TIMEOUT),
            'data': json.dumps({'ip': request.client.host, 'message': 'Pierwsze połączenie' if lastEventId == '$' else 'Ponowne połączenie'}),
            'id': '-1',
        }

        lid = lastEventId

        while True:
            if await request.is_disconnected():
                break

            try:
                resps = await rc.xread({SSE_EVENT_NAME: lid}, count=10, block=STATUS_STREAM_RETRY_TIMEOUT)

                if not resps:
                    continue

                for resp in resps:
                    event, messages = resp
                    lastEventId, data = messages[0]

                    yield {
                        'event': SSE_EVENT_NAME,
                        'retry': jitter_timeout_sec(STATUS_STREAM_RETRY_TIMEOUT),
                        'data': json.dumps(data),
                        'id': lastEventId
                    }
                    lid = lastEventId
            except (ConnectionError, TimeoutError, RedisError) as ex:
                break
    finally:
        await asyncio.sleep(jitter_timeout_sec(STATUS_STREAM_RETRY_TIMEOUT) / 1_000)

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
    platform_user: str = request.headers.get('sec-ch-ua-platform', 'nieznany')
    await rc.xadd(SSE_EVENT_NAME, {'task': 'put_one_item', 'ip': request.client.host, 'message': f'Użytkownik {platform_user} na PyCon2025 PL'}, maxlen=20, approximate=False)

@app.get('/stream')
async def stream(request: Request, rc: redis.Redis = Depends(get_redis_client)):
    lastEventId = request.headers.get('last-event-id', '$')

    event_generator = events_generator(request, rc, lastEventId)
    return EventSourceResponse(event_generator)
