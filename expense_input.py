"""記帳輸入模組：輸入支出（日期、金額、類別、備註）並存到 expenses.csv"""
import csv
import os
from datetime import date, datetime

# 資料檔放在程式同一個資料夾，不管從哪裡執行都找得到
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "expenses.csv")
FIELDS = ["date", "amount", "category", "note"]
CATEGORIES = ["餐飲", "交通", "購物", "娛樂", "住宿", "其他"]


def ask_date():
    """輸入日期，直接按 Enter 代表今天"""
    while True:
        text = input(f"日期 (YYYY-MM-DD，直接按 Enter = 今天 {date.today()}): ").strip()
        if text == "":
            return date.today().isoformat()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("  格式錯誤，請輸入像 2026-11-25 這樣的日期。")


def ask_amount():
    """輸入金額，必須是大於 0 的數字"""
    while True:
        text = input("金額: ").strip()
        try:
            amount = float(text)
        except ValueError:
            print("  請輸入數字。")
            continue
        if amount <= 0:
            print("  金額必須大於 0。")
            continue
        return amount


def ask_category():
    """從清單選類別，或自己輸入新類別"""
    for i, name in enumerate(CATEGORIES, 1):
        print(f"  {i}. {name}")
    while True:
        text = input("類別 (輸入編號，或直接打新類別名稱): ").strip()
        if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
            return CATEGORIES[int(text) - 1]
        if text and not text.isdigit():
            return text
        print("  請輸入清單中的編號或類別名稱。")


def save_expense(expense):
    """把一筆支出加到 CSV 檔最後面，檔案不存在就先寫標題列"""
    is_new = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(expense)


def load_expenses():
    """讀出所有支出紀錄"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_expense():
    print("\n--- 新增支出 ---")
    expense = {
        "date": ask_date(),
        "amount": ask_amount(),
        "category": ask_category(),
        "note": input("備註 (可留空): ").strip(),
    }
    save_expense(expense)
    print(f"已儲存：{expense['date']} {expense['category']} {expense['amount']:g} 元")


def list_expenses():
    rows = load_expenses()
    if not rows:
        print("\n目前沒有任何紀錄。")
        return
    print("\n日期          金額      類別    備註")
    total = 0
    for r in rows:
        amount = float(r["amount"])
        total += amount
        print(f"{r['date']}  {amount:>8g}  {r['category']:<6}{r['note']}")
    print(f"共 {len(rows)} 筆，總計 {total:g} 元")


def main():
    while True:
        print("\n=== 記帳工具 ===")
        print("1. 新增支出")
        print("2. 查看所有紀錄")
        print("0. 離開")
        choice = input("請選擇: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "0":
            print("再見！")
            break
        else:
            print("請輸入 0、1 或 2。")


if __name__ == "__main__":
    main()