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
from trading_agent_os.evaluation.submissions import (
    build_registry_rows,
    validate_submission,
    validate_submission_file,
    write_registry_html,
    write_registry_markdown,
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
    "build_registry_rows",
    "export_audit_bundle",
    "validate_submission",
    "validate_submission_file",
    "write_registry_html",
    "write_registry_markdown",
]
