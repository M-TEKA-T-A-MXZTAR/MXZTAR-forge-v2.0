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


def _base_polygon(item: dict) -> list[tuple[float, float]]:
    """Return the same bounded primitive outline used by the CPU viewport."""
    width = float(item["size"]["x"])
    height = float(item["size"]["y"])
    primitive = item["primitive_type"]
    if primitive in {"rectangle", "square"}:
        return [
            (-width / 2.0, -height / 2.0),
            (width / 2.0, -height / 2.0),
            (width / 2.0, height / 2.0),
            (-width / 2.0, height / 2.0),
        ]
    if primitive in {"circle", "ellipse"}:
        return [
            (
                math.cos(index * math.tau / 24.0) * width / 2.0,
                math.sin(index * math.tau / 24.0) * height / 2.0,
            )
            for index in range(24)
        ]
    if primitive == "star":
        parameters = item.get("primitive_parameters", {})
        points = int(parameters.get("points", 5))
        inner_ratio = float(parameters.get("inner_ratio", 0.45))
        result = []
        for index in range(points * 2):
            angle = -math.pi / 2.0 + index * math.pi / points
            ratio = 1.0 if index % 2 == 0 else inner_ratio
            result.append(
                (
                    math.cos(angle) * width / 2.0 * ratio,
                    math.sin(angle) * height / 2.0 * ratio,
                )
            )
        return result
    raise ValueError(f"Unsupported guide primitive: {primitive!r}.")


def _rotated_local_bounds(item: dict) -> dict[str, tuple[float, float]]:
    """Derive viewport-matching local AABB offsets after object rotation."""
    rotation = item["rotation_deg"]
    rx = math.radians(float(rotation["x"]))
    ry = math.radians(float(rotation["y"]))
    rz = math.radians(float(rotation["z"]))
    cosine_x, sine_x = math.cos(rx), math.sin(rx)
    cosine_y, sine_y = math.cos(ry), math.sin(ry)
    cosine_z, sine_z = math.cos(rz), math.sin(rz)

    def rotate(point: tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = point
        y, z = y * cosine_x - z * sine_x, y * sine_x + z * cosine_x
        x, z = x * cosine_y + z * sine_y, -x * sine_y + z * cosine_y
        x, y = x * cosine_z - y * sine_z, x * sine_z + y * cosine_z
        return x, y, z

    depth = float(item["size"]["z"])
    points = []
    for x, y in _base_polygon(item):
        points.append(rotate((x, y, -depth / 2.0)))
        points.append(rotate((x, y, depth / 2.0)))
    return {
        axis: (
            min(point[index] for point in points),
            max(point[index] for point in points),
        )
        for index, axis in enumerate(AXES)
    }


def _object_features(item: dict) -> dict[str, dict[str, float]]:
    local_bounds = _rotated_local_bounds(item)
    result = {}
    for axis in AXES:
        center = float(item["position"][axis])
        local_min, local_max = local_bounds[axis]
        result[axis] = {
            "min": center + local_min,
            "center": center,
            "max": center + local_max,
        }
    return result


def _axis_surface_gap(first: dict[str, float], second: dict[str, float]) -> float:
    return max(
        0.0,
        first["min"] - second["max"],
        second["min"] - first["max"],
    )


def _nearest_object(
    moving: dict,
    moving_features: dict[str, dict[str, float]],
    others: list[tuple[dict, dict[str, dict[str, float]]]],
) -> dict | None:
    if not others:
        return None
    moving_position = moving["position"]
    best: dict | None = None
    for item, item_features in others:
        deltas = {
            axis: float(item["position"][axis]) - float(moving_position[axis])
            for axis in AXES
        }
        center_distance = math.sqrt(sum(value * value for value in deltas.values()))
        surface_axis_gaps = {
            axis: _axis_surface_gap(moving_features[axis], item_features[axis])
            for axis in AXES
        }
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
    moving_features: dict[str, dict[str, float]],
    others: list[tuple[dict, dict[str, dict[str, float]]]],
    scene_center: dict[str, float],
    axis: str,
) -> dict:
    references = [
        {
            "reference_kind": "scene_center",
            "reference_object_id": None,
            "reference_feature": "center",
            "reference_value": float(scene_center[axis]),
        }
    ]
    for item, item_features in others:
        for feature, value in item_features[axis].items():
            references.append(
                {
                    "reference_kind": "object",
                    "reference_object_id": item["object_id"],
                    "reference_feature": feature,
                    "reference_value": value,
                }
            )

    candidates = []
    for moving_feature, moving_value in moving_features[axis].items():
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

    Guide calculations use axis-aligned bounds derived from the same rotated primitive
    geometry rendered by the CPU viewport. They never mutate the input object or any
    nonselected scene member.
    """
    bounded_tolerance = clamp_snap_tolerance(tolerance)
    updated = copy.deepcopy(moving_object)
    object_id = updated["object_id"]
    other_items = [
        copy.deepcopy(item)
        for item in scene_objects
        if item.get("object_id") != object_id
    ]
    others = [(item, _object_features(item)) for item in other_items]
    center = dict(zip(AXES, (float(value) for value in scene_center), strict=True))

    alignments = []
    snap_applied = False
    for axis in AXES:
        candidate = _alignment_candidate(_object_features(updated), others, center, axis)
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
    moving_features = _object_features(updated)
    guide_state = {
        "object_id": object_id,
        "tolerance": bounded_tolerance,
        "snap_enabled": bool(snap_enabled),
        "snap_applied": snap_applied,
        "scene_center": center,
        "scene_delta": scene_delta,
        "nearest": _nearest_object(updated, moving_features, others),
        "alignments": alignments,
    }
    return updated, guide_state
