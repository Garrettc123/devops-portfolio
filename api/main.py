"""FastAPI Router — primary API gateway for the agent swarm."""
import json
import os
import uuid
from contextlib import asynccontextmanager
from typing import Any, Dict

import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await aioredis.from_url(
        os.getenv("REDIS_URL", "redis://redis:6379"), decode_responses=True)
    yield
    await app.state.redis.close()


app = FastAPI(title="Zero-Human Enterprise Grid — Swarm API Router",
              version="1.0.0", lifespan=lifespan)

AGENT_IDS = ["data-ingestion-agent", "logic-planning-agent",
             "code-execution-agent", "system-monitor-agent"]


class TaskRequest(BaseModel):
    source: str
    payload: Dict[str, Any]
    priority: int = 3


@app.post("/task")
async def dispatch_task(req: TaskRequest):
    task_id = str(uuid.uuid4())
    await app.state.redis.publish("channel:raw_data", json.dumps(
        {"task_id": task_id, "source": req.source,
         "payload": req.payload, "priority": req.priority}))
    return {"task_id": task_id, "status": "dispatched", "channel": "channel:raw_data"}


@app.get("/health")
async def health_check():
    agents = {aid: (await app.state.redis.get(f"agent:heartbeat:{aid}") or "DEAD")
              for aid in AGENT_IDS}
    try:
        await app.state.redis.ping()
        redis_ok = True
    except Exception:
        redis_ok = False
    return {"status": "healthy" if all(v != "DEAD" for v in agents.values()) and redis_ok else "degraded",
            "agents": agents, "redis": "OK" if redis_ok else "ERROR"}


@app.get("/task/{task_id}/status")
async def task_status(task_id: str):
    result = await app.state.redis.hget("health:task_ledger", task_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return {"task_id": task_id, **json.loads(result)}


@app.get("/")
async def root():
    return {"service": "Swarm API Router", "version": "1.0.0", "status": "online"}
