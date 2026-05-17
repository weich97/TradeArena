"""TradeArena public package alias.

The historical implementation package is still named ``trading_agent_os``.
This module keeps the public package identity aligned with the PyPI/project
name while preserving backward compatibility for existing imports.
"""

from __future__ import annotations

import importlib
import sys

from trading_agent_os import *  # noqa: F403


_ALIASES = (
    "agents",
    "core",
    "data",
    "evaluation",
    "factory",
    "memory",
    "planning",
    "tools",
)

for _name in _ALIASES:
    _module = importlib.import_module(f"trading_agent_os.{_name}")
    sys.modules[f"{__name__}.{_name}"] = _module
    globals()[_name] = _module
