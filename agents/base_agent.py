"""BaseAgent — abstract base class for all swarm agents."""
import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional

import redis.asyncio as aioredis

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")


class BaseAgent(ABC):
    def __init__(self, agent_id: str, input_channel: str, output_channel: str):
        self.agent_id = agent_id
        self.input_channel = input_channel
        self.output_channel = output_channel
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
        self.redis: Optional[aioredis.Redis] = None
        self.pubsub = None
        self.logger = logging.getLogger(self.agent_id)
        self.running = False

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(self.input_channel)
        self.logger.info(f"Connected. Subscribed to [{self.input_channel}]")

    async def publish(self, payload: Dict[str, Any]):
        payload["source_agent"] = self.agent_id
        payload["timestamp"] = datetime.utcnow().isoformat()
        await self.redis.publish(self.output_channel, json.dumps(payload))
        self.logger.info(f"Published to [{self.output_channel}]")

    async def heartbeat(self):
        while self.running:
            await self.redis.setex(f"agent:heartbeat:{self.agent_id}", 30, datetime.utcnow().isoformat())
            await asyncio.sleep(10)

    @abstractmethod
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def run(self):
        await self.connect()
        self.running = True
        asyncio.create_task(self.heartbeat())
        self.logger.info(f"Agent [{self.agent_id}] running")
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    result = await self.process(data)
                    if result:
                        await self.publish(result)
                except Exception as e:
                    self.logger.error(f"Processing error: {e}", exc_info=True)

    async def stop(self):
        self.running = False
        if self.pubsub:
            await self.pubsub.unsubscribe(self.input_channel)
        if self.redis:
            await self.redis.close()
