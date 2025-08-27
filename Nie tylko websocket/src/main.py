import asyncio
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/events")
async def stream_events():
    async def event_generator():
        counter = 0
        while True:
            data = dict(message=f"Hello from server! Count: {counter}")
            yield f"data: {json.dumps(data)}\n\n"
            counter += 1
            await asyncio.sleep(1)
    
    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
