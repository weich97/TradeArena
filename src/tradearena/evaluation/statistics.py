from __future__ import annotations

import math
import random
from collections.abc import Iterable, Mapping
from typing import Any


def mean(values: Iterable[float]) -> float:
    numbers = [float(value) for value in values]
    return sum(numbers) / len(numbers) if numbers else 0.0


def sample_std(values: Iterable[float]) -> float:
    numbers = [float(value) for value in values]
    if len(numbers) < 2:
        return 0.0
    center = mean(numbers)
    return math.sqrt(sum((value - center) ** 2 for value in numbers) / (len(numbers) - 1))


def bootstrap_ci(
    values: Iterable[float],
    *,
    confidence: float = 0.95,
    draws: int = 2000,
    seed: int = 1729,
) -> tuple[float | None, float | None]:
    numbers = [float(value) for value in values]
    if not numbers:
        return None, None
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    rng = random.Random(seed)
    boot_means = []
    for _ in range(max(1, draws)):
        sample = [numbers[rng.randrange(len(numbers))] for _ in numbers]
        boot_means.append(mean(sample))
    boot_means.sort()
    alpha = max(0.0, min(1.0, 1.0 - confidence))
    lower_index = min(len(boot_means) - 1, max(0, int((alpha / 2.0) * len(boot_means))))
    upper_index = min(len(boot_means) - 1, max(0, int((1.0 - alpha / 2.0) * len(boot_means)) - 1))
    return boot_means[lower_index], boot_means[upper_index]


def summarize_metric(values: Iterable[float], *, prefix: str) -> dict[str, float | None]:
    numbers = [float(value) for value in values]
    ci_low, ci_high = bootstrap_ci(numbers)
    return {
        f"{prefix}_mean": mean(numbers),
        f"{prefix}_std": sample_std(numbers),
        f"{prefix}_ci_low": ci_low,
        f"{prefix}_ci_high": ci_high,
    }


def paired_bootstrap_difference(
    candidate_by_key: Mapping[Any, float],
    baseline_by_key: Mapping[Any, float],
    *,
    confidence: float = 0.95,
    draws: int = 2000,
    seed: int = 2026,
) -> dict[str, float | int | None]:
    keys = sorted(set(candidate_by_key) & set(baseline_by_key), key=str)
    differences = [float(candidate_by_key[key]) - float(baseline_by_key[key]) for key in keys]
    if not differences:
        return {
            "paired_n": 0,
            "mean_delta": None,
            "delta_ci_low": None,
            "delta_ci_high": None,
            "p_value": None,
        }
    ci_low, ci_high = bootstrap_ci(differences, confidence=confidence, draws=draws, seed=seed)
    rng = random.Random(seed + 1)
    boot_means = []
    for _ in range(max(1, draws)):
        sample = [differences[rng.randrange(len(differences))] for _ in differences]
        boot_means.append(mean(sample))
    less_or_equal_zero = sum(1 for value in boot_means if value <= 0.0) / len(boot_means)
    greater_or_equal_zero = sum(1 for value in boot_means if value >= 0.0) / len(boot_means)
    p_value = min(1.0, 2.0 * min(less_or_equal_zero, greater_or_equal_zero))
    return {
        "paired_n": len(differences),
        "mean_delta": mean(differences),
        "delta_ci_low": ci_low,
        "delta_ci_high": ci_high,
        "p_value": p_value,
    }

