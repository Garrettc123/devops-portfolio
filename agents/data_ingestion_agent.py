"""DataIngestionAgent — pulls, normalizes, and routes raw data into the swarm."""
import asyncio
from typing import Any, Dict
from base_agent import BaseAgent


class DataIngestionAgent(BaseAgent):
    CHANNEL_IN = "channel:raw_data"
    CHANNEL_OUT = "channel:normalized_data"

    def __init__(self):
        super().__init__("data-ingestion-agent", self.CHANNEL_IN, self.CHANNEL_OUT)

    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Ingesting payload keys: {list(message.keys())}")
        return {
            "task_id": message.get("task_id", "unknown"),
            "source": message.get("source", "unknown"),
            "payload": message.get("payload", {}),
            "priority": message.get("priority", 3),
            "schema_version": "1.0",
            "status": "ingested",
        }


if __name__ == "__main__":
    asyncio.run(DataIngestionAgent().run())
