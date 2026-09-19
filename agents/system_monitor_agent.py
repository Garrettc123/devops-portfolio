"""SystemMonitorAgent — health ledger, heartbeat polling, anomaly alerts."""
import asyncio
import json
from typing import Any, Dict
from base_agent import BaseAgent


class SystemMonitorAgent(BaseAgent):
    CHANNEL_IN = "channel:execution_results"
    CHANNEL_OUT = "channel:alerts"
    FAILURE_THRESHOLD = 3
    AGENT_IDS = ["data-ingestion-agent", "logic-planning-agent", "code-execution-agent"]

    def __init__(self):
        super().__init__("system-monitor-agent", self.CHANNEL_IN, self.CHANNEL_OUT)
        self._failures: Dict[str, int] = {}

    async def _heartbeats(self) -> Dict[str, str]:
        return {aid: (await self.redis.get(f"agent:heartbeat:{aid}") or "DEAD")
                for aid in self.AGENT_IDS}

    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        task_id, status = message.get("task_id"), message.get("overall_status", "unknown")
        if status != "success":
            self._failures[task_id] = self._failures.get(task_id, 0) + 1
        else:
            self._failures.pop(task_id, None)
        await self.redis.hset("health:task_ledger", task_id,
                              json.dumps({"status": status, "failures": self._failures.get(task_id, 0)}))
        hb = await self._heartbeats()
        dead = [a for a, v in hb.items() if v == "DEAD"]
        if self._failures.get(task_id, 0) >= self.FAILURE_THRESHOLD:
            return {"type": "TASK_FAILURE_THRESHOLD", "task_id": task_id, "failures": self._failures[task_id]}
        if dead:
            return {"type": "AGENT_DOWN", "dead_agents": dead}
        return None


if __name__ == "__main__":
    asyncio.run(SystemMonitorAgent().run())
