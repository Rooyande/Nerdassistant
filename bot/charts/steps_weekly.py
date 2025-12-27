from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def build_steps_weekly_chart(entries, out_dir: str = "/tmp") -> str:
    """
    entries: لیست StepEntry (day, steps)
    خروجی: مسیر فایل PNG
    """
    if not entries:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        out_path = os.path.join(out_dir, "steps_weekly_empty.png")

        plt.figure(figsize=(7, 3))
        plt.title("Steps Weekly Report")
        plt.text(0.5, 0.5, "No steps data yet.", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()
        return out_path

    dates = [e.day.strftime("%m-%d") for e in entries]
    steps = [e.steps for e in entries]

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_path = os.path.join(out_dir, f"steps_weekly_{int(datetime.utcnow().timestamp())}.png")

    plt.figure(figsize=(8, 4))
    plt.title("Steps (Last 7 Days)")
    plt.xlabel("Day")
    plt.ylabel("Steps")

    plt.plot(dates, steps, marker="o")
    plt.grid(True, linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

    return out_path
