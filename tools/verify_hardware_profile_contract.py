#!/usr/bin/env python3
"""
Verify adaptive hardware policy classification for MXZTAR Forge v2.0.

This verifier does not require special hardware. It uses synthetic HardwareSpec
objects to prove that unknown and modest rigs stay safe while capable rigs can
receive a higher, bounded thread recommendation.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from core.hardware_profile import (  # noqa: E402
    BYTES_PER_GIB,
    HardwareSpec,
    apply_local_ai_policy,
    classify_hardware,
    parse_meminfo,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def bytes_gib(value: int) -> int:
    return value * BYTES_PER_GIB


def verify_unknown_safe_mode() -> None:
    policy = classify_hardware(
        HardwareSpec(
            logical_cpus=0,
            total_ram_bytes=0,
            available_ram_bytes=0,
            detection_notes=("synthetic unknown",),
        )
    )

    require(policy.profile_key == "UNKNOWN_SAFE_MODE", "unknown hardware must use safe mode")
    require(policy.ollama_num_thread == 2, "unknown hardware must use two safe threads")
    require(policy.ollama_num_parallel == 1, "unknown hardware must use one parallel job")
    require(policy.max_heavy_jobs == 1, "unknown hardware must allow one heavy job")

    print("PASS: unknown hardware falls back safely")


def verify_modest_cpu_only() -> None:
    policy = classify_hardware(
        HardwareSpec(
            logical_cpus=4,
            total_ram_bytes=bytes_gib(8),
            available_ram_bytes=bytes_gib(3),
            detection_notes=("synthetic modest",),
        )
    )

    require(policy.profile_key == "MODEST_CPU_ONLY", "modest rig must use modest CPU profile")
    require(policy.ollama_num_thread <= 2, "modest rig must not exceed two threads")
    require(policy.ollama_num_parallel == 1, "modest rig must use one parallel job")
    require(policy.max_heavy_jobs == 1, "modest rig must allow one heavy job")

    print("PASS: modest CPU-only hardware stays conservative")


def verify_capable_cpu_only() -> None:
    policy = classify_hardware(
        HardwareSpec(
            logical_cpus=16,
            total_ram_bytes=bytes_gib(32),
            available_ram_bytes=bytes_gib(16),
            detection_notes=("synthetic capable",),
        )
    )

    require(policy.profile_key == "CAPABLE_CPU_ONLY", "capable CPU rig not detected")
    require(4 <= policy.ollama_num_thread <= 8, "capable CPU thread count must be bounded")
    require(policy.ollama_num_parallel == 1, "capable CPU rig must still use one parallel job")
    require(policy.max_heavy_jobs == 1, "capable CPU rig must still use one heavy job")

    print("PASS: capable CPU-only hardware adapts within bounds")


def verify_gpu_present() -> None:
    policy = classify_hardware(
        HardwareSpec(
            logical_cpus=16,
            total_ram_bytes=bytes_gib(64),
            available_ram_bytes=bytes_gib(24),
            gpu_detected=True,
            gpu_name="Synthetic GPU",
            detection_notes=("synthetic gpu",),
        )
    )

    require(policy.profile_key == "GPU_AVAILABLE", "GPU rig not detected")
    require(policy.gpu_detected, "GPU flag must be preserved")
    require(policy.gpu_name == "Synthetic GPU", "GPU name must be preserved")
    require(policy.ollama_num_parallel == 1, "GPU presence must not silently raise parallel jobs")
    require(policy.max_heavy_jobs == 1, "GPU presence must not silently raise heavy jobs")

    print("PASS: GPU hardware is detected without unsafe parallel escalation")


def verify_meminfo_parser() -> None:
    total, available = parse_meminfo(
        "MemTotal:       16384000 kB\n"
        "MemAvailable:   8192000 kB\n"
    )

    require(total == 16384000 * 1024, "MemTotal parse failed")
    require(available == 8192000 * 1024, "MemAvailable parse failed")

    print("PASS: Linux meminfo parser works")


def verify_env_application() -> None:
    original_thread = os.environ.get("OLLAMA_NUM_THREAD")
    original_parallel = os.environ.get("OLLAMA_NUM_PARALLEL")

    try:
        policy = classify_hardware(
            HardwareSpec(
                logical_cpus=8,
                total_ram_bytes=bytes_gib(24),
                available_ram_bytes=bytes_gib(8),
                detection_notes=("synthetic env",),
            )
        )
        applied = apply_local_ai_policy(policy)

        require(applied == policy, "applied policy should be returned")
        require(os.environ["OLLAMA_NUM_THREAD"] == str(policy.ollama_num_thread), "thread env not applied")
        require(os.environ["OLLAMA_NUM_PARALLEL"] == str(policy.ollama_num_parallel), "parallel env not applied")
    finally:
        if original_thread is None:
            os.environ.pop("OLLAMA_NUM_THREAD", None)
        else:
            os.environ["OLLAMA_NUM_THREAD"] = original_thread

        if original_parallel is None:
            os.environ.pop("OLLAMA_NUM_PARALLEL", None)
        else:
            os.environ["OLLAMA_NUM_PARALLEL"] = original_parallel

    print("PASS: selected policy applies Ollama environment")


def main() -> int:
    print("MXZTAR Forge Hardware Profile Contract Verification")
    verify_unknown_safe_mode()
    verify_modest_cpu_only()
    verify_capable_cpu_only()
    verify_gpu_present()
    verify_meminfo_parser()
    verify_env_application()
    print("PASS: hardware profile contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
