from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # مهم: برای اجرا داخل سرور بدون UI

import matplotlib.pyplot as plt


def _minutes_to_hours(minutes: int) -> float:
    return round(minutes / 60.0, 2)


def build_sleep_weekly_chart(sessions, out_dir: str = "/tmp") -> str:
    """
    sessions: لیست SleepSession که gn_at و gm_at دارند (gm_at ممکنه None باشه)
    خروجی: مسیر فایل PNG
    """
    # فقط سشن‌هایی که GM دارند (یعنی خواب کامل شده)
    completed = [s for s in sessions if s.gm_at is not None]
    if not completed:
        # یک تصویر ساده با پیام
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        out_path = os.path.join(out_dir, "sleep_weekly_empty.png")

        plt.figure(figsize=(7, 3))
        plt.title("Sleep Weekly Report")
        plt.text(0.5, 0.5, "No completed sleep sessions yet.", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()
        return out_path

    # آماده‌سازی داده‌ها
    dates = []
    hours = []

    for s in completed:
        # تاریخ را با gn_at نمایش می‌دهیم
        d = s.gn_at.date()
        duration_min = int((s.gm_at - s.gn_at).total_seconds() // 60)
        if duration_min < 0:
            duration_min = 0
        dates.append(d.strftime("%m-%d"))
        hours.append(_minutes_to_hours(duration_min))

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_path = os.path.join(out_dir, f"sleep_weekly_{int(datetime.utcnow().timestamp())}.png")

    plt.figure(figsize=(8, 4))
    plt.title("Sleep (Last 7 Days)")
    plt.xlabel("Day")
    plt.ylabel("Hours")

    plt.plot(dates, hours, marker="o")
    plt.grid(True, linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

    return out_path
