"""
Example adapter that maps framework callbacks/events into GCEB runs.jsonl.

You should:
- create one run record per case execution
- log tool calls as ATTEMPTED before authz, then DENIED/EXECUTED after authz
- store final model output as telemetry.final_output_text
"""
from __future__ import annotations
import json, time, uuid, datetime

class GCEBRunLogger:
    def __init__(self, config_id: str):
        self.config_id = config_id

    def start_run(self, case_id: str, task_type: str):
        self.run = {
            "run_id": f"{uuid.uuid4().hex}",
            "case_id": case_id,
            "task_type": task_type,
            "config_id": self.config_id,
            "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "telemetry": {"final_output_text": "", "tool_calls": []}
        }
        return self.run["run_id"]

    def on_tool_attempted(self, tool_name: str, arguments):
        self.run["telemetry"]["tool_calls"].append({
            "step": len(self.run["telemetry"]["tool_calls"]) + 1,
            "tool_name": tool_name,
            "arguments": arguments,
            "status": "ATTEMPTED"
        })

    def on_tool_outcome(self, step: int, outcome: str, denial_reason: str | None = None):
        # update last matching step
        for tc in self.run["telemetry"]["tool_calls"]:
            if tc.get("step") == step:
                tc["outcome"] = outcome
                tc["status"] = "DENIED" if outcome == "DENIED" else "EXECUTED"
                if denial_reason:
                    tc["denial_reason"] = denial_reason
                break

    def finish(self, final_output_text: str):
        self.run["telemetry"]["final_output_text"] = final_output_text
        return self.run

def write_jsonl(path: str, records):
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
