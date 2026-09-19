"""LogicPlanningAgent — Symbolic Engine: validates + decomposes tasks into execution plans."""
import asyncio
from typing import Any, Dict, List
from base_agent import BaseAgent


class LogicPlanningAgent(BaseAgent):
    CHANNEL_IN = "channel:normalized_data"
    CHANNEL_OUT = "channel:execution_plan"
    CONSTRAINT_RULES = [
        lambda t: t.get("schema_version") == "1.0",
        lambda t: t.get("task_id") not in (None, "unknown"),
        lambda t: isinstance(t.get("payload"), dict),
    ]

    def __init__(self):
        super().__init__("logic-planning-agent", self.CHANNEL_IN, self.CHANNEL_OUT)

    def _validate(self, task: Dict[str, Any]) -> bool:
        for rule in self.CONSTRAINT_RULES:
            if not rule(task):
                self.logger.warning(f"Constraint FAILED for [{task.get('task_id')}]")
                return False
        return True

    def _build_plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"step": i+1, "action": a, "params": p, "status": "pending"}
                for i, (a, p) in enumerate(task.get("payload", {}).items())]

    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        if not self._validate(message):
            return {"task_id": message.get("task_id"), "status": "rejected", "reason": "constraint_failure"}
        plan = self._build_plan(message)
        return {"task_id": message.get("task_id"), "execution_plan": plan,
                "priority": message.get("priority", 3), "status": "planned"}


if __name__ == "__main__":
    asyncio.run(LogicPlanningAgent().run())
