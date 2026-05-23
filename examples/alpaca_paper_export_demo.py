from __future__ import annotations

from pathlib import Path

from tradearena.core.domain import Order, OrderType, Side
from tradearena.core.serialization import write_json
from tradearena.tools import AlpacaPaperExportAdapter

OUTPUT_DIR = Path("outputs/examples/alpaca_paper_export")


def main() -> int:
    orders = [
        Order("AAPL", Side.BUY, 12.5, reason="approved target-weight rebalance"),
        Order("MSFT", Side.SELL, 3.0, OrderType.LIMIT, limit_price=420.0, reason="trim concentration after risk review"),
        Order("SGOV", Side.HOLD, 0.0, reason="no trade needed"),
    ]
    adapter = AlpacaPaperExportAdapter(client_prefix="demo-review")
    result = adapter.write(orders, OUTPUT_DIR)
    summary = {
        **result,
        "live_submission": False,
        "safety_note": "Generated files are paper-review exports only; they are not submitted to Alpaca or any broker.",
    }
    write_json(OUTPUT_DIR / "summary.json", summary)
    print("Alpaca paper export demo")
    print(f"  orders={summary['order_count']} paper_only={summary['paper_only']}")
    print(f"  wrote={summary['json']}")
    print(f"  wrote={summary['csv']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
