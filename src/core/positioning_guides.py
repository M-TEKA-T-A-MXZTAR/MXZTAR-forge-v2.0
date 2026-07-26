#!/usr/bin/env python3
"""Deterministic transient positioning guides for Forge object movement."""

from __future__ import annotations

import copy
import math


MIN_SNAP_TOLERANCE = 1.0
MAX_SNAP_TOLERANCE = 50.0
DEFAULT_SNAP_TOLERANCE = 12.0
AXES = ("x", "y", "z")
FEATURES = ("min", "center", "max")


def clamp_snap_tolerance(value: float) -> float:
    """Return a bounded scene-unit tolerance without accepting booleans."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("Guide snap tolerance must be numeric.")
    return max(MIN_SNAP_TOLERANCE, min(MAX_SNAP_TOLERANCE, float(value)))


def _axis_features(item: dict, axis: str) -> dict[str, float]:
    center = float(item["position"][axis])
    half_size = float(item["size"][axis]) / 2.0
    return {
        "min": center - half_size,
        "center": center,
        "max": center + half_size,
    }


def _nearest_object(moving: dict, others: list[dict]) -> dict | None:
    if not others:
        return None
    moving_position = moving["position"]
    moving_size = moving["size"]
    best: dict | None = None
    for item in others:
        deltas = {
            axis: float(item["position"][axis]) - float(moving_position[axis])
            for axis in AXES
        }
        center_distance = math.sqrt(sum(value * value for value in deltas.values()))
        surface_axis_gaps = {}
        for axis in AXES:
            half_extent = (
                float(moving_size[axis]) + float(item["size"][axis])
            ) / 2.0
            surface_axis_gaps[axis] = max(0.0, abs(deltas[axis]) - half_extent)
        surface_distance = math.sqrt(
            sum(value * value for value in surface_axis_gaps.values())
        )
        candidate = {
            "object_id": item["object_id"],
            "center_distance": center_distance,
            "surface_distance": surface_distance,
            "axis_delta": deltas,
        }
        if best is None or candidate["center_distance"] < best["center_distance"]:
            best = candidate
    return best


def _alignment_candidate(
    moving: dict,
    others: list[dict],
    scene_center: dict[str, float],
    axis: str,
) -> dict:
    moving_features = _axis_features(moving, axis)
    references = [
        {
            "reference_kind": "scene_center",
            "reference_object_id": None,
            "reference_feature": "center",
            "reference_value": float(scene_center[axis]),
        }
    ]
    for item in others:
        for feature, value in _axis_features(item, axis).items():
            references.append(
                {
                    "reference_kind": "object",
                    "reference_object_id": item["object_id"],
                    "reference_feature": feature,
                    "reference_value": value,
                }
            )

    candidates = []
    for moving_feature, moving_value in moving_features.items():
        for reference in references:
            delta = reference["reference_value"] - moving_value
            candidates.append(
                {
                    "axis": axis,
                    "moving_feature": moving_feature,
                    **reference,
                    "delta": delta,
                    "distance": abs(delta),
                }
            )
    return min(
        candidates,
        key=lambda value: (
            value["distance"],
            0 if value["reference_kind"] == "object" else 1,
            FEATURES.index(value["moving_feature"]),
        ),
    )


def calculate_positioning_guides(
    moving_object: dict,
    scene_objects: list[dict],
    scene_center: tuple[float, float, float],
    *,
    tolerance: float = DEFAULT_SNAP_TOLERANCE,
    snap_enabled: bool = False,
) -> tuple[dict, dict]:
    """Calculate transient guide evidence and optionally snap X/Y movement.

    Guide calculations are derived from axis-aligned object bounds in current scene
    units. They never mutate the input object or any nonselected scene member.
    """
    bounded_tolerance = clamp_snap_tolerance(tolerance)
    updated = copy.deepcopy(moving_object)
    object_id = updated["object_id"]
    others = [
        copy.deepcopy(item)
        for item in scene_objects
        if item.get("object_id") != object_id
    ]
    center = dict(zip(AXES, (float(value) for value in scene_center), strict=True))

    alignments = []
    snap_applied = False
    for axis in AXES:
        candidate = _alignment_candidate(updated, others, center, axis)
        if candidate["distance"] <= bounded_tolerance:
            if snap_enabled and axis in {"x", "y"} and candidate["delta"] != 0.0:
                updated["position"][axis] = (
                    float(updated["position"][axis]) + candidate["delta"]
                )
                snap_applied = True
                candidate = {**candidate, "snapped": True, "delta": 0.0, "distance": 0.0}
            else:
                candidate = {**candidate, "snapped": False}
            alignments.append(candidate)

    scene_delta = {
        axis: float(updated["position"][axis]) - center[axis]
        for axis in AXES
    }
    guide_state = {
        "object_id": object_id,
        "tolerance": bounded_tolerance,
        "snap_enabled": bool(snap_enabled),
        "snap_applied": snap_applied,
        "scene_center": center,
        "scene_delta": scene_delta,
        "nearest": _nearest_object(updated, others),
        "alignments": alignments,
    }
    return updated, guide_state
