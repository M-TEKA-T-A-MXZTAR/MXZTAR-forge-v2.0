#!/usr/bin/env python3
"""
Adaptive local hardware profile for MXZTAR Forge v2.0.

The policy is conservative by design:
- unknown machines fall back to the safe CPU-only profile;
- GPU detection is recorded but does not silently enable parallel heavy jobs;
- local AI settings are recommendations applied through explicit runtime values;
- no model downloads or long-running probes are triggered here.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

BYTES_PER_GIB = 1024 ** 3
SAFE_CPU_THREADS = 2
SAFE_PARALLEL_JOBS = 1


@dataclass(frozen=True)
class HardwareSpec:
    logical_cpus: int
    total_ram_bytes: int
    available_ram_bytes: int
    gpu_detected: bool = False
    gpu_name: str = ""
    detection_notes: Tuple[str, ...] = ()


@dataclass(frozen=True)
class LocalAIPolicy:
    profile_key: str
    profile_label: str
    ollama_num_thread: int
    ollama_num_parallel: int
    max_heavy_jobs: int
    recommended_model_size: str
    gpu_detected: bool
    gpu_name: str
    notes: Tuple[str, ...]

    def env(self) -> dict[str, str]:
        return {
            "OLLAMA_NUM_THREAD": str(self.ollama_num_thread),
            "OLLAMA_NUM_PARALLEL": str(self.ollama_num_parallel),
        }


def clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def gib(bytes_value: int) -> float:
    return bytes_value / BYTES_PER_GIB if bytes_value > 0 else 0.0


def parse_meminfo(text: str) -> tuple[int, int]:
    values: dict[str, int] = {}

    for line in text.splitlines():
        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        parts = raw_value.strip().split()

        if not parts:
            continue

        try:
            kib = int(parts[0])
        except ValueError:
            continue

        values[key] = kib * 1024

    total = values.get("MemTotal", 0)
    available = values.get("MemAvailable", total)
    return total, available


def read_linux_memory(meminfo_path: Path = Path("/proc/meminfo")) -> tuple[int, int]:
    try:
        return parse_meminfo(meminfo_path.read_text(encoding="utf-8"))
    except OSError:
        return 0, 0


def command_output(command: list[str], timeout_seconds: float = 1.0) -> str:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except (OSError, subprocess.SubprocessError):
        return ""

    return (completed.stdout or completed.stderr or "").strip()


def detect_gpu() -> tuple[bool, str, tuple[str, ...]]:
    notes: list[str] = []

    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        output = command_output(
            [nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
            timeout_seconds=1.5,
        )
        first_line = output.splitlines()[0].strip() if output else "NVIDIA GPU"
        notes.append("nvidia-smi detected")
        return True, first_line, tuple(notes)

    rocm_smi = shutil.which("rocm-smi")
    if rocm_smi:
        notes.append("rocm-smi detected")
        return True, "AMD/ROCm GPU", tuple(notes)

    if Path("/dev/dri").exists():
        notes.append("/dev/dri detected")
        return True, "Linux DRI GPU", tuple(notes)

    notes.append("no GPU probe matched")
    return False, "", tuple(notes)


def detect_hardware() -> HardwareSpec:
    logical_cpus = os.cpu_count() or 1
    total_ram, available_ram = read_linux_memory()
    gpu_detected, gpu_name, gpu_notes = detect_gpu()

    notes = [
        f"logical_cpus={logical_cpus}",
        f"total_ram_gib={gib(total_ram):.1f}",
        f"available_ram_gib={gib(available_ram):.1f}",
        *gpu_notes,
    ]

    return HardwareSpec(
        logical_cpus=max(1, logical_cpus),
        total_ram_bytes=max(0, total_ram),
        available_ram_bytes=max(0, available_ram),
        gpu_detected=gpu_detected,
        gpu_name=gpu_name,
        detection_notes=tuple(notes),
    )


def classify_hardware(spec: HardwareSpec) -> LocalAIPolicy:
    cpus = max(1, spec.logical_cpus)
    total_gib = gib(spec.total_ram_bytes)
    available_gib = gib(spec.available_ram_bytes)
    notes = list(spec.detection_notes)

    if spec.total_ram_bytes <= 0:
        notes.append("memory unknown; using safe fallback")
        return LocalAIPolicy(
            profile_key="UNKNOWN_SAFE_MODE",
            profile_label="Unknown hardware — safe mode",
            ollama_num_thread=SAFE_CPU_THREADS,
            ollama_num_parallel=SAFE_PARALLEL_JOBS,
            max_heavy_jobs=1,
            recommended_model_size="small vision model",
            gpu_detected=spec.gpu_detected,
            gpu_name=spec.gpu_name,
            notes=tuple(notes),
        )

    if cpus <= 4 or total_gib < 12 or available_gib < 4:
        notes.append("low/modest resource envelope")
        return LocalAIPolicy(
            profile_key="MODEST_CPU_ONLY",
            profile_label="Modest CPU-only safe profile",
            ollama_num_thread=clamp_int(min(cpus, SAFE_CPU_THREADS), 1, SAFE_CPU_THREADS),
            ollama_num_parallel=1,
            max_heavy_jobs=1,
            recommended_model_size="small vision model",
            gpu_detected=spec.gpu_detected,
            gpu_name=spec.gpu_name,
            notes=tuple(notes),
        )

    if spec.gpu_detected and cpus >= 8 and total_gib >= 24 and available_gib >= 8:
        notes.append("gpu present; keeping one heavy job by default")
        return LocalAIPolicy(
            profile_key="GPU_AVAILABLE",
            profile_label="GPU-capable profile",
            ollama_num_thread=clamp_int(cpus // 2, 4, 8),
            ollama_num_parallel=1,
            max_heavy_jobs=1,
            recommended_model_size="medium vision model if already installed",
            gpu_detected=True,
            gpu_name=spec.gpu_name,
            notes=tuple(notes),
        )

    if cpus >= 8 and total_gib >= 24 and available_gib >= 8:
        notes.append("capable CPU envelope")
        return LocalAIPolicy(
            profile_key="CAPABLE_CPU_ONLY",
            profile_label="Capable CPU-only profile",
            ollama_num_thread=clamp_int(cpus // 2, 4, 8),
            ollama_num_parallel=1,
            max_heavy_jobs=1,
            recommended_model_size="small or medium vision model",
            gpu_detected=spec.gpu_detected,
            gpu_name=spec.gpu_name,
            notes=tuple(notes),
        )

    notes.append("defaulting to modest safe profile")
    return LocalAIPolicy(
        profile_key="MODEST_CPU_ONLY",
        profile_label="Modest CPU-only safe profile",
        ollama_num_thread=SAFE_CPU_THREADS,
        ollama_num_parallel=1,
        max_heavy_jobs=1,
        recommended_model_size="small vision model",
        gpu_detected=spec.gpu_detected,
        gpu_name=spec.gpu_name,
        notes=tuple(notes),
    )


def policy_summary(policy: LocalAIPolicy) -> str:
    gpu_text = f", GPU: {policy.gpu_name}" if policy.gpu_detected and policy.gpu_name else ""
    return (
        f"{policy.profile_label}: threads={policy.ollama_num_thread}, "
        f"parallel={policy.ollama_num_parallel}, heavy_jobs={policy.max_heavy_jobs}, "
        f"model={policy.recommended_model_size}{gpu_text}"
    )


def get_local_ai_policy() -> LocalAIPolicy:
    return classify_hardware(detect_hardware())


def apply_local_ai_policy(policy: LocalAIPolicy | None = None) -> LocalAIPolicy:
    selected = policy or get_local_ai_policy()
    for key, value in selected.env().items():
        os.environ[key] = value
    return selected
