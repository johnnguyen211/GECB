# GCEB

Benchmark scaffold + dataset.

## Structure
- datasets/: dataset files
- schemas/: json schemas
- scorer/: scoring scripts
- harness/: adapter examples
- paper/: paper draft

## Quickstart
```bash
python scorer/score_runs.py --pred runs.jsonl --cases datasets/cases.jsonl
