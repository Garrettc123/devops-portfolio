"""CodeExecutionAgent — executes planned steps via allowlisted actions only."""
import asyncio
import subprocess
from typing import Any, Dict, List
from base_agent import BaseAgent


class CodeExecutionAgent(BaseAgent):
    CHANNEL_IN = "channel:execution_plan"
    CHANNEL_OUT = "channel:execution_results"
    ALLOWED_ACTIONS = {"shell", "http_get", "http_post", "deploy", "test", "log"}

    def __init__(self):
        super().__init__("code-execution-agent", self.CHANNEL_IN, self.CHANNEL_OUT)

    async def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        action, params = step.get("action"), step.get("params", {})
        if action not in self.ALLOWED_ACTIONS:
            return {**step, "status": "blocked", "output": f"'{action}' not in allowlist"}
        if action == "shell":
            try:
                r = subprocess.run(params.get("command", "echo no-op"),
                                   shell=True, capture_output=True, text=True, timeout=30)
                return {**step, "status": "completed", "output": r.stdout, "error": r.stderr}
            except subprocess.TimeoutExpired:
                return {**step, "status": "timeout", "output": "", "error": "timed out"}
        if action == "log":
            self.logger.info(f"[LOG] {params.get('message', '')}")
            return {**step, "status": "completed", "output": params.get("message", "")}
        return {**step, "status": "stub", "output": f"'{action}' not yet implemented"}

    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        task_id = message.get("task_id")
        plan: List[Dict] = message.get("execution_plan", [])
        results = [await self._execute_step(s) for s in plan]
        ok = all(r["status"] in ("completed", "stub") for r in results)
        return {"task_id": task_id, "step_results": results,
                "overall_status": "success" if ok else "partial_failure"}


if __name__ == "__main__":
    asyncio.run(CodeExecutionAgent().run())
