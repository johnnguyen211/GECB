# GCEB — Ghost Canary Exfiltration Benchmark

This repository contains a reproducible benchmark for evaluating **tool-connected / connector-enabled AI agents** against **Indirect Prompt Injection (IPI)**.

## What’s inside

- `datasets/` — workload files (released dataset)
  - `datasets/cases.jsonl` — 1,000 cases (attack+benign)
  - `datasets/manifest.json` — dataset metadata
- `schemas/` — JSON Schemas for portable telemetry
  - `cases.schema.json`
  - `runs.schema.json`
- `scorer/` — deterministic canary-based scoring (Leak + PBV)
  - `score_runs.py`
- `harness/` — minimal harness + adapter pattern (example)
  - `adapter_example.py`
- `paper/` — draft paper source

## Quick start (scoring)

1) Put your run traces at `runs.jsonl` (one JSON object per run).
2) Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scorer/score_runs.py \
  --cases datasets/cases.jsonl \
  --runs runs.jsonl \
  --out scored_runs.jsonl
```

This emits:
- `scored_runs.jsonl` (per-run labels: `is_leak`, `is_pbv`, `asr_success`, etc.)
- a printed summary with LR / PBVR / ASR / FPR.

## Telemetry contract (runs.jsonl)

Each run should log:
- `run_id`, `case_id`, `task_type`, `config_id`, `timestamp`
- `telemetry.final_output_text`
- `telemetry.tool_calls[]` (with `tool_name`, `arguments`, `status` = `ATTEMPTED|DENIED|EXECUTED`)

See `schemas/runs.schema.json` and `examples/runs_example.json`.

## License

Choose a license before publishing (MIT/Apache-2.0 are common).
