---
title: ER Triage Environment
sdk: docker
app_port: 8000
base_path: /web
tags:
  - openenv
---

# ER Triage Environment

An OpenEnv environment where an AI agent triages emergency room patients using the Emergency Severity Index (ESI) protocol. The agent gathers information (vitals, history) and assigns a priority level, balancing speed and accuracy.

**Live Space:** https://huggingface.co/spaces/hawkaii/er_triage

## Architecture

![Architecture](pics/architecture.png)

## Tasks

Three tasks with increasing difficulty:

| Task | Difficulty | Description |
|------|-----------|-------------|
| `single_triage` | Easy | Triage 1 patient |
| `batch_triage` | Medium | Triage 3 patients sequentially |
| `differential_triage` | Hard | Triage 1 patient with misleading symptoms |

## Action / Observation Space

**Action** (`ERTriageAction`):
- `action_type`: `request_vitals` | `ask_question` | `assign_priority`
- `question` (optional): clarifying question for the patient
- `priority` (optional): `critical` | `urgent` | `non-urgent`
- `reasoning`: agent's rationale

**Observation** (`ERTriageObservation`):
- `patient_id`, `chief_complaint`, `available_actions`
- `vitals` (dict, after requesting), `question_answer` (str, after asking)
- `reward`, `done`

## Reward Function

Partial progress rewards in [0, 1]:

| Action | Reward |
|--------|--------|
| `request_vitals` | +0.2 |
| `ask_question` | +0.1 |
| `assign_priority` (correct) | +0.7 |
| `assign_priority` (wrong) | 0.0 |

Max per patient: **1.0** (vitals + question + correct priority)

## Setup

```bash
# Install dependencies
uv sync

# Run server locally
uv run server

# Build Docker image
docker build -t er_triage-env:latest -f server/Dockerfile .

# Deploy to HF Spaces
openenv push --repo-id <your-username>/er_triage
```

## Running Inference

```bash
export HF_TOKEN=<your-token>
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

TASK_NAME=single_triage python inference.py
TASK_NAME=batch_triage python inference.py
TASK_NAME=differential_triage python inference.py
```

Structured output format:
```
[START] task=single_triage env=er_triage model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=request_vitals reward=0.20 done=false error=null
[STEP] step=2 action=ask_question('describe symptoms') reward=0.10 done=false error=null
[STEP] step=3 action=assign_priority(critical) reward=0.70 done=true error=null
[END] success=true steps=3 score=1.000 rewards=0.20,0.10,0.70
```

![Inference Logs](pics/inferenece_logs.png)

## Deployed Environment

![HF Spaces](pics/environment_huggingface_spaces.png)

## Project Structure

```
ER_Triage/
├── inference.py           # LLM-powered inference (OpenAI client)
├── client.py              # ERTriageEnv client
├── models.py              # Action and Observation models
├── openenv.yaml           # OpenEnv manifest
├── pyproject.toml         # Dependencies
├── data/
│   └── patients.py        # 11 patients (3 tricky for hard task)
├── server/
│   ├── er_triage_environment.py  # Core environment logic
│   ├── app.py             # FastAPI server
│   └── Dockerfile
└── pics/                  # Screenshots and diagrams
```
