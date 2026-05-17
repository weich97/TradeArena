from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs/examples"
DEMO_VIDEO_ASSET = ROOT / "docs/assets/tradearena_3min_demo.mp4"
DEMO_VIDEO_POSTER = ROOT / "docs/assets/tradearena_3min_demo_thumbnail.png"


SECTIONS = [
    (
        "First-run portal",
        "Start with a guided quickstart route through the main demo artifacts, their source commands, and redacted cache manifest.",
        "index.html",
        "python scripts/run_launch_demo.py",
    ),
    (
        "Experiment-design demos",
        "Execution realism, Markowitz/MVO baselines, representation signatures, and custom plugin extensibility.",
        "experiment_design_index.html",
        "python scripts/run_paper_design_demos.py",
    ),
    (
        "Animated visual tour",
        "Regenerate the README animations and inspect what each preview conveys without relying on motion alone.",
        "visual_tour_index.html",
        "python examples/visual_tour_demo.py",
    ),
    (
        "Audit report",
        "Trace one decision from market observation through proposal, risk review, execution, and reflection.",
        "audit_report.html",
        "python scripts/render_audit_report.py",
    ),
    (
        "Crisis gallery",
        "Representation trajectory, correlation/intent heatmap, feedback curves, and exposure waterfall snapshots.",
        "crisis_snapshot_gallery.html",
        "python examples/crisis_snapshot_demo.py",
    ),
    (
        "A-share rule stress",
        "T+1, price-limit, and board-lot constraints as auditable risk-gate interventions.",
        "ashare_market_rules.svg",
        "python examples/ashare_market_rules_demo.py",
    ),
    (
        "Custom plugin extension",
        "A local analyst plugin running through the same strategy, risk, execution, memory, and evaluator stack.",
        "custom_plugin.svg",
        "python examples/custom_plugin_demo.py",
    ),
    (
        "Contributor extension walkthrough",
        "Swap in a custom analyst, risk manager, and evaluator while reusing the rest of the framework.",
        "extension_walkthrough.svg",
        "python examples/extension_walkthrough_demo.py",
    ),
    (
        "Retail planning sandbox",
        "Review investor profiles, suitability checks, target allocations, futures margin estimates, and paper rebalance orders.",
        "retail_planning_report.html",
        "python examples/retail_planner_demo.py",
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public-facing TradeArena showcase.")
    parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="Only write the showcase index from existing artifacts; do not rerun demos.",
    )
    args = parser.parse_args()

    print("TradeArena showcase", flush=True)
    print("===================", flush=True)
    print("A one-command quickstart repo tour for new users, reviewers, and launch posts.", flush=True)

    if not args.reuse_existing:
        _run([sys.executable, "scripts/run_launch_demo.py", "--skip-paper-figures"], "Launch demo portal")
        _run([sys.executable, "scripts/run_paper_design_demos.py"], "Experiment-design demo suite")
        _run([sys.executable, "examples/visual_tour_demo.py"], "Animated visual tour")
        _run([sys.executable, "examples/extension_walkthrough_demo.py"], "Contributor extension walkthrough")
        _run([sys.executable, "examples/retail_planner_demo.py"], "Retail planning sandbox")

    _write_demo_video_page()
    _write_showcase_index(OUTPUT_DIR / "showcase.html")
    print("\nShowcase artifacts", flush=True)
    print("------------------", flush=True)
    for _, _, href, _ in SECTIONS:
        path = OUTPUT_DIR / href
        print(f"[{'ok' if path.exists() else 'missing'}] outputs/examples/{href}", flush=True)
    print(f"[{'ok' if (OUTPUT_DIR / 'demo_video.html').exists() else 'missing'}] outputs/examples/demo_video.html", flush=True)
    print(f"[{'ok' if (OUTPUT_DIR / 'tradearena_3min_demo.mp4').exists() else 'missing'}] outputs/examples/tradearena_3min_demo.mp4", flush=True)
    print("[ok] outputs/examples/showcase.html", flush=True)
    return 0


def _run(command: list[str], label: str) -> None:
    print(f"\n{label}", flush=True)
    print("-" * len(label), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def _write_demo_video_page() -> None:
    if not DEMO_VIDEO_ASSET.exists():
        raise FileNotFoundError(
            f"Missing demo video asset: {DEMO_VIDEO_ASSET}. Run python scripts/build_demo_video.py first."
        )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DEMO_VIDEO_ASSET, OUTPUT_DIR / "tradearena_3min_demo.mp4")
    poster_html = ""
    if DEMO_VIDEO_POSTER.exists():
        shutil.copy2(DEMO_VIDEO_POSTER, OUTPUT_DIR / "tradearena_3min_demo_thumbnail.png")
        poster_html = ' poster="tradearena_3min_demo_thumbnail.png"'
    html = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TradeArena 3-Minute Demo Video</title>
<style>
body {{ margin: 0; font-family: Inter, Arial, sans-serif; background: #0f172a; color: #e2e8f0; }}
main {{ max-width: 1120px; margin: 0 auto; padding: 40px 24px 54px; }}
a {{ color: #67e8f9; }}
h1 {{ margin: 0 0 8px; font-size: 38px; letter-spacing: 0; }}
.lead {{ margin: 0 0 22px; max-width: 850px; color: #cbd5e1; line-height: 1.55; }}
.video-wrap {{ border: 1px solid #334155; border-radius: 12px; overflow: hidden; background: #020617; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35); }}
video {{ display: block; width: 100%; height: auto; background: #020617; }}
.links {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}
.links a {{ display: inline-block; padding: 9px 12px; border: 1px solid #334155; border-radius: 8px; background: #111827; text-decoration: none; font-weight: 700; }}
</style>
<main>
  <h1>TradeArena 3-Minute Demo Video</h1>
  <p class="lead">A captioned walkthrough of the quickstart command, showcase portal, audit report, execution realism, extension walkthrough, and retail planning sandbox. This static Pages video plays in the browser and does not require downloading a release asset.</p>
  <div class="video-wrap">
    <video controls preload="metadata"{poster_html}>
      <source src="tradearena_3min_demo.mp4" type="video/mp4">
      Your browser does not support embedded MP4 video. Open <a href="tradearena_3min_demo.mp4">the MP4 file</a>.
    </video>
  </div>
  <div class="links">
    <a href="showcase.html">Back to showcase</a>
    <a href="audit_report.html">Audit report</a>
    <a href="extension_walkthrough.svg">Extension walkthrough</a>
    <a href="retail_planning_report.html">Retail planning</a>
  </div>
</main>
</html>
"""
    (OUTPUT_DIR / "demo_video.html").write_text(html, encoding="utf-8")


def _write_showcase_index(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cards = "\n".join(_card_html(title, body, href, command) for title, body, href, command in SECTIONS)
    html = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>TradeArena Showcase: Quickstart Tour</title>
<style>
body {{ margin: 0; font-family: Inter, Arial, sans-serif; background: #f8fafc; color: #0f172a; }}
main {{ max-width: 1080px; margin: 0 auto; padding: 44px 28px 54px; }}
h1 {{ margin: 0 0 8px; font-size: 36px; letter-spacing: 0; }}
.lead {{ margin: 0 0 18px; max-width: 820px; color: #475569; line-height: 1.58; }}
.strip {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 26px; }}
.pill {{ border: 1px solid #cbd5e1; border-radius: 999px; padding: 6px 10px; background: #ffffff; color: #334155; font-size: 12px; font-weight: 700; }}
.video-spotlight {{ display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(260px, 0.75fr); gap: 18px; align-items: stretch; margin: 0 0 22px; padding: 18px; border: 1px solid #cbd5e1; border-radius: 10px; background: #0f172a; color: #e2e8f0; box-shadow: 0 20px 48px rgba(15, 23, 42, 0.16); }}
.video-spotlight video {{ display: block; width: 100%; height: auto; border-radius: 8px; background: #020617; }}
.video-copy {{ padding: 4px 4px 0; }}
.video-copy h2 {{ margin: 0 0 8px; font-size: 24px; letter-spacing: 0; color: #ffffff; }}
.video-copy p {{ margin: 0 0 14px; color: #cbd5e1; line-height: 1.5; font-size: 14px; }}
.video-links {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.video-links a {{ display: inline-block; padding: 8px 10px; border-radius: 7px; border: 1px solid #334155; background: #111827; color: #ccfbf1; text-decoration: none; font-size: 12px; font-weight: 800; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 14px; }}
.card {{ display: block; min-height: 154px; padding: 18px; border: 1px solid #d8e2ed; border-radius: 8px; background: white; color: inherit; text-decoration: none; }}
.card:hover {{ border-color: #2563eb; box-shadow: 0 12px 28px rgba(15, 23, 42, 0.10); transform: translateY(-1px); }}
.card span {{ display: block; font-weight: 800; font-size: 16px; margin-bottom: 8px; }}
.card p {{ margin: 0 0 12px; color: #64748b; font-size: 13px; line-height: 1.45; }}
.command {{ display: inline-block; padding: 6px 8px; border-radius: 6px; background: #f1f5f9; color: #334155; font-size: 12px; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }}
.footer {{ margin-top: 26px; color: #64748b; font-size: 13px; line-height: 1.5; }}
@media (max-width: 820px) {{ .video-spotlight {{ grid-template-columns: 1fr; }} }}
</style>
<main>
  <h1>TradeArena Showcase: Quickstart Tour</h1>
  <p class="lead">Run one command, open one page, and inspect the artifacts that demonstrate auditable trajectories, realistic execution, risk gates, diagnostic visuals, and extensible plugins. Each card names the artifact and the command that regenerates it, and the showcase path requires no API keys or live provider calls.</p>
  <div class="strip">
    <span class="pill">No API key required</span>
    <span class="pill">Execution realism</span>
    <span class="pill">Risk lifecycle</span>
    <span class="pill">Replayable trajectories</span>
    <span class="pill">Extensible plugins</span>
  </div>
  <section class="video-spotlight" aria-label="TradeArena 3-minute demo video">
    <video controls preload="metadata" poster="tradearena_3min_demo_thumbnail.png">
      <source src="tradearena_3min_demo.mp4" type="video/mp4">
      Your browser does not support embedded MP4 video. Open <a href="tradearena_3min_demo.mp4">the MP4 file</a>.
    </video>
    <div class="video-copy">
      <h2>3-Minute Demo Video</h2>
      <p>Watch the quickstart command, showcase portal, audit report, execution realism, extension walkthrough, and retail planning sandbox without leaving this page.</p>
      <div class="video-links">
        <a href="demo_video.html">Open theater view</a>
        <a href="tradearena_3min_demo.mp4">Open MP4</a>
      </div>
    </div>
  </section>
  <section class="grid">
    {cards}
  </section>
  <p class="footer">Generated by <code>python scripts/run_showcase.py</code>. Large model calls and live market-data downloads are intentionally outside the first-run path.</p>
</main>
</html>
"""
    path.write_text(html, encoding="utf-8")
    print(f"\nWrote {path.relative_to(ROOT)}", flush=True)


def _card_html(title: str, body: str, href: str, command: str) -> str:
    status = "ready" if (OUTPUT_DIR / href).exists() else "generate first"
    return (
        f'<a class="card" href="{href}">'
        f"<span>{title}</span>"
        f"<p>{body}</p>"
        f'<code class="command">{command}</code>'
        f'<p style="margin-top:10px">Artifact status: {status}</p>'
        "</a>"
    )


if __name__ == "__main__":
    raise SystemExit(main())
