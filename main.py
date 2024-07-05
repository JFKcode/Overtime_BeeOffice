import tkinter as tk
from tkinter import ttk
from logic import AppLogic
from overtime import add_overtime

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Overtime")

        # Styl
        style = ttk.Style(self)
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'), ('active', 'white')])
        style.configure("TCombobox", padding=6)

        self.logic = AppLogic(self)

        # Numer id
        tk.Label(self, text="Numer użytkownika").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_number = tk.Entry(self)
        self.user_number.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.logic.set_user_number_entry(self.user_number)

        # Data
        tk.Label(self, text="Wybierz dzień").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = self.logic.create_date_entry()
        self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # godzina od
        tk.Label(self, text="Godzina od").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.time_from_hour, self.time_from_minute = self.logic.create_time_entry()
        self.time_from_hour.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.time_from_minute.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # godzina do
        tk.Label(self, text="Godzina do").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.time_to_hour, self.time_to_minute = self.logic.create_time_entry()
        self.time_to_hour.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.time_to_minute.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Dodanie danych do listy
        self.add_button = ttk.Button(self, text="Dodaj dane", command=self.logic.add_data)
        self.add_button.grid(row=4, column=0, columnspan=3, pady=(10, 5))

        # Usuwanie z listy
        self.delete_button = ttk.Button(self, text="Usuń zaznaczone dane", command=self.logic.delete_data)
        self.delete_button.grid(row=5, column=0, columnspan=3, pady=(5, 5))

        # Odpalenie skryptu i dodanie nadgodzin
        self.overtime_button = ttk.Button(self, text="Dodaj nadgodziny", command=self.logic.add_overtime)
        self.overtime_button.grid(row=6, column=0, columnspan=3, pady=(5, 10))

        # Lista dodanych danych
        self.data_list = tk.Listbox(self, selectmode=tk.MULTIPLE, height=10, width=60)
        self.data_list.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.logic.initialize_listbox(self.data_list)
        self.logic.load_data()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
