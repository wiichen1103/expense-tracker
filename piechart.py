import csv
import os
import sys
from collections import defaultdict

import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "expenses.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "pie_chart.png")

# 讓 matplotlib 可以顯示中文（Windows / Mac 字型都列進去）
plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei", "PingFang TC", "Heiti TC",
    "Noto Sans CJK TC", "Arial Unicode MS",
]
plt.rcParams["axes.unicode_minus"] = False


def load_totals(path):
    """讀取 CSV，依類別加總金額"""
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            try:
                amount = float(row["amount"])
                if amount > 0:
                    totals[row["category"]] += amount
            except (KeyError, ValueError):
                print(f"略過格式錯誤的資料：{row}")
    return dict(totals)


def draw_pie(totals):
    """畫圓餅圖，由大到小排列，並存成 pie_chart.png"""
    items = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    labels = [k for k, _ in items]
    values = [v for _, v in items]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        values,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({p * total / 100:.0f} 元)",
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white"},
    )
    ax.set_title(f"各類別支出比例（總計 {total:.0f} 元）")
    ax.axis("equal")
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)
    print(f"圓餅圖已存成 {OUTPUT_FILE}")
    plt.show()


def main():
    if not os.path.exists(DATA_FILE):
        print("找不到 expenses.csv，請先執行 python expense_input.py 新增支出。")
        sys.exit(1)
    totals = load_totals(DATA_FILE)
    if not totals:
        print("expenses.csv 裡沒有資料。")
        sys.exit(1)
    draw_pie(totals)


if __name__ == "__main__":
    main()