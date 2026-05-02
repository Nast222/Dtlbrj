import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_training():
    date = date_entry.get()
    training_type = type_entry.get()
    duration = duration_entry.get()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
        return

    try:
        duration = float(duration)
        if duration <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return

    data.append({"date": date, "type": training_type, "duration": duration})
    save_data(data)
    update_table()
    clear_entries()

def update_table(filter_date=None, filter_type=None):
    for i in treeview.get_children():
        treeview.delete(i)
    for item in data:
        if filter_date and item["date"] != filter_date:
            continue
        if filter_type and item["type"] != filter_type:
            continue
        treeview.insert("", "end", values=(item["date"], item["type"], item["duration"]))

def clear_entries():
    date_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)

# Загрузка данных
data = load_data()

# Окно
root = tk.Tk()
root.title("Training Planner")
root.geometry("700x400")

# Поля ввода
tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=10, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Тип тренировки:").grid(row=1, column=0, padx=10, pady=5)
type_entry = tk.Entry(root)
type_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Длительность (мин):").grid(row=2, column=0, padx=10, pady=5)
duration_entry = tk.Entry(root)
duration_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Добавить тренировку", command=add_training).grid(row=3, column=0, columnspan=2, pady=10)

# Таблица
treeview = ttk.Treeview(root, columns=("Дата", "Тип", "Длительность"), show="headings")
treeview.heading("Дата", text="Дата")
treeview.heading("Тип", text="Тип")
treeview.heading("Длительность", text="Длительность (мин)")
treeview.grid(row=4, column=0, columnspan=2, padx=10, sticky="nsew")

# Фильтры
tk.Label(root, text="Фильтр по дате:").grid(row=5, column=0, padx=10, pady=5)
filter_date = tk.Entry(root)
filter_date.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Фильтр по типу:").grid(row=6, column=0, padx=10, pady=5)
filter_type = tk.Entry(root)
filter_type.grid(row=6, column=1, padx=10, pady=5)

def apply_filter():
    update_table(filter_date.get() or None, filter_type.get() or None)

tk.Button(root, text="Применить фильтр", command=apply_filter).grid(row=7, column=0, columnspan=2, pady=10)

# Заполнение таблицы при запуске
update_table()
root.mainloop()
