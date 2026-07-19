#!/usr/bin/env python3
"""
MXZTAR Forge v2.0 Ollama HTTP service.

Uses Ollama's local HTTP API, not the unavailable `ollama generate` command.

Hardware-kind policy:
- qwen2.5vl:3b remains the default local vision model;
- runtime CPU thread count is selected by the adaptive hardware profile;
- parallel heavy jobs remain capped at one by default.
"""

import base64
import json
from dataclasses import dataclass
from pathlib import Path

import requests

from brain.prompts import build_prompt
from core.hardware_profile import apply_local_ai_policy


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
    return encode_image_bytes_base64(path.read_bytes())


def encode_image_bytes_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def run_vision_workflow(
    source_path: Path,
    workflow_key: str,
    user_notes: str = "",
    model: str = DEFAULT_MODEL,
    timeout_seconds: int = 600,
    image_bytes: bytes | None = None,
) -> AgentResult:
    ai_policy = apply_local_ai_policy()

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
        "images": [
            encode_image_bytes_base64(image_bytes)
            if image_bytes is not None
            else encode_image_base64(source_path)
        ],
        "stream": False,
        "options": {
            "num_thread": ai_policy.ollama_num_thread,
            "temperature": 0.35,
            "num_predict": 1200,
        },
    }

    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json=payload,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        body = response.text
    except requests.exceptions.RequestException as exc:
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
