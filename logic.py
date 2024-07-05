import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import csv
import os
from datetime import datetime


class AppLogic:
    def __init__(self, parent):
        self.parent = parent
        self.data_list = None

    def set_user_number_entry(self, entry):
        self.user_number = entry
        vcmd = (self.parent.register(self.validate_id_length), '%P')
        self.user_number.config(validate='key', validatecommand=vcmd)

    def create_date_entry(self):
        return DateEntry(self.parent, date_pattern='y-mm-dd')

    def create_time_entry(self):
        vcmd = (self.parent.register(self.validate_time_entry), '%P')

        hour = ttk.Combobox(self.parent, values=[f"{i:02d}" for i in range(24)], width=3, validate='key',
                            validatecommand=vcmd)
        minute = ttk.Combobox(self.parent, values=[f"{i:02d}" for i in range(60)], width=3, validate='key',
                              validatecommand=vcmd)

        hour.bind('<FocusOut>', lambda e: self.format_time_entry(hour, 'hour'))
        minute.bind('<FocusOut>', lambda e: self.format_time_entry(minute, 'minute'))

        return hour, minute

    def initialize_listbox(self, listbox):
        self.data_list = listbox

    def is_user_in_login_csv(self, user_number):
        if os.path.exists('loginy.csv'):
            with open('loginy.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == user_number:
                        return True
        return False

    def add_data(self):
        user_number = self.user_number.get()

        if len(user_number) != 5:
            messagebox.showerror("Error", "The ID number must contain exactly 5 digits.")
            return

        if not self.is_user_in_login_csv(user_number):
            messagebox.showerror("Error", "No ID specified in the database.")
            return

        date = self.parent.date_entry.get()
        time_from = f"{self.parent.time_from_hour.get()}:{self.parent.time_from_minute.get()}"
        time_to = f"{self.parent.time_to_hour.get()}:{self.parent.time_to_minute.get()}"

        try:
            with open('data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_number, date, time_from, time_to])
        except PermissionError:
            messagebox.showerror("Error", "No permission to write to 'data.csv' file.")

        self.data_list.insert(tk.END, f"{user_number}, {date}, {time_from}, {time_to}")

        # Czyszczenie pól formularza
        self.clear_entries()

    def load_data(self):
        if os.path.exists('data.csv'):
            try:
                with open('data.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        self.data_list.insert(tk.END, f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")
            except PermissionError:
                messagebox.showerror("Error", "No permission to read file 'data.csv'.")

    def delete_data(self):
        selected_indices = self.data_list.curselection()
        data = self.data_list.get(0, tk.END)

        for index in reversed(selected_indices):
            self.data_list.delete(index)

        try:
            with open('data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for index, row in enumerate(data):
                    if index not in selected_indices:
                        writer.writerow(row.split(", "))
        except PermissionError:
            messagebox.showerror("Error", "No permission to write to 'data.csv' file.")

    def add_overtime(self):
        print("Add overtime")

    def validate_id_length(self, P):
        if len(P) > 5:
            return False
        return P.isdigit()

    def validate_time_entry(self, P):
        if len(P) > 2:
            return False
        return P.isdigit()

    def format_time_entry(self, entry, type):
        value = entry.get()
        if value.isdigit() and len(value) == 1:
            entry.set(f"0{value}")
        elif value.isdigit() and len(value) == 2:
            entry.set(value)
        elif type == 'minute' and value == '':
            entry.set('00')
        else:
            entry.set('')

    def clear_entries(self):
        # Wyłączenie walidacji przed czyszczeniem
        self.user_number.config(validate='none')
        self.user_number.delete(0, tk.END)
        self.user_number.config(validate='key')
        self.parent.date_entry.set_date(datetime.now())
        self.parent.time_from_hour.set('')
        self.parent.time_from_minute.set('')
        self.parent.time_to_hour.set('')
        self.parent.time_to_minute.set('')
