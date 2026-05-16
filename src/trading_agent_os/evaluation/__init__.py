"""Evaluation and benchmark plugins."""

from trading_agent_os.evaluation.benchmarks import BenchmarkCase, BenchmarkRunner
from trading_agent_os.evaluation.audit import AuditManifest, export_audit_bundle
from trading_agent_os.evaluation.metrics import (
    BehavioralEvaluator,
    ExecutionRealismEvaluator,
    PerformanceEvaluator,
    ReasoningConsistencyEvaluator,
    RiskAuditEvaluator,
)
from trading_agent_os.evaluation.tasks import BenchmarkTask, DataLeakagePolicy, TRADEARENA_CORE_TASKS

__all__ = [
    "AuditManifest",
    "BehavioralEvaluator",
    "BenchmarkCase",
    "BenchmarkRunner",
    "BenchmarkTask",
    "DataLeakagePolicy",
    "ExecutionRealismEvaluator",
    "PerformanceEvaluator",
    "ReasoningConsistencyEvaluator",
    "RiskAuditEvaluator",
    "TRADEARENA_CORE_TASKS",
    "export_audit_bundle",
]
