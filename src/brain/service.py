#!/usr/bin/env python3
"""
MXZTAR-forge v2c0 Ollama HTTP service.

Uses Ollama's local HTTP API, not the unavailable `ollama generate` command.

Hardware-kind defaults:
- qwen2.5vl:3b
- 2 CPU threads
- 1 parallel AI job
"""

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from brain.prompts import build_prompt


DEFAULT_MODEL = "qwen2.5vl:3b"
OLLAMA_GENERATE_URL = "http://127.0.0.1:11434/api/generate"


@dataclass
class AgentResult:
    ok: bool
    model: str
    workflow_key: str
    source_path: str
    output_text: str
    error: str = ""


def encode_image_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def run_vision_workflow(
    source_path: Path,
    workflow_key: str,
    user_notes: str = "",
    model: str = DEFAULT_MODEL,
    timeout_seconds: int = 600,
) -> AgentResult:
    os.environ["OLLAMA_NUM_THREAD"] = "2"
    os.environ["OLLAMA_NUM_PARALLEL"] = "1"

    source_path = Path(source_path).expanduser().resolve()

    if not source_path.exists():
        return AgentResult(
            ok=False,
            model=model,
            workflow_key=workflow_key,
            source_path=str(source_path),
            output_text="",
            error=f"Source image not found: {source_path}",
        )

    prompt = build_prompt(
        workflow_key=workflow_key,
        source_path=str(source_path),
        user_notes=user_notes,
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "images": [encode_image_base64(source_path)],
        "stream": False,
        "options": {
            "num_thread": 2,
            "temperature": 0.35,
            "num_predict": 1200,
        },
    }

    request = urllib.request.Request(
        OLLAMA_GENERATE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        return AgentResult(
            ok=False,
            model=model,
            workflow_key=workflow_key,
            source_path=str(source_path),
            output_text="",
            error=f"Could not reach Ollama HTTP API: {exc}",
        )
    except Exception as exc:
        return AgentResult(
            ok=False,
            model=model,
            workflow_key=workflow_key,
            source_path=str(source_path),
            output_text="",
            error=f"Ollama request failed: {exc}",
        )

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return AgentResult(
            ok=False,
            model=model,
            workflow_key=workflow_key,
            source_path=str(source_path),
            output_text=body,
            error="Ollama returned non-JSON response.",
        )

    if "error" in parsed:
        return AgentResult(
            ok=False,
            model=model,
            workflow_key=workflow_key,
            source_path=str(source_path),
            output_text="",
            error=str(parsed["error"]),
        )

    response_text = str(parsed.get("response", "")).strip()

    if not response_text:
        return AgentResult(
            ok=False,
            model=model,
            workflow_key=workflow_key,
            source_path=str(source_path),
            output_text="",
            error="Ollama returned no response text.",
        )

    return AgentResult(
        ok=True,
        model=model,
        workflow_key=workflow_key,
        source_path=str(source_path),
        output_text=response_text,
        error="",
    )
