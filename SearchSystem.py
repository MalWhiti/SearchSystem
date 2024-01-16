import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Добавить рейс', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_edit_dialog = tk.Button(toolbar, text='Редактировать рейс', bg='#d7d8e0', bd=0, compound=tk.TOP,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Удалить рейс', bg='#d7d8e0', bd=0, compound=tk.TOP,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, compound=tk.TOP,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, compound=tk.TOP,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        btn_number_seats = tk.Button(toolbar, text='Подсчитать количество билетов', bg='#d7d8e0', bd=0, compound=tk.TOP,
                                command=self.open_seats_dialog)
        btn_number_seats.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('number', 'from_where', 'to_where', 'departure_date', 'departure_time',
                                                'flight_time'), height=15, show='headings')

        self.tree.column('number', width=100, anchor=tk.CENTER)
        self.tree.column('from_where', width=100, anchor=tk.CENTER)
        self.tree.column('to_where', width=100, anchor=tk.CENTER)
        self.tree.column('departure_date', width=100, anchor=tk.CENTER)
        self.tree.column('departure_time', width=100, anchor=tk.CENTER)
        self.tree.column('flight_time', width=100, anchor=tk.CENTER)

        self.tree.heading('number', text='Номер рейса')
        self.tree.heading('from_where', text='Откуда')
        self.tree.heading('to_where', text='Куда')
        self.tree.heading('departure_date', text='Когда')
        self.tree.heading('departure_time', text='Во сколько')
        self.tree.heading('flight_time', text='Время в пути', command=lambda: sort(5, False))

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        def sort(col, reverse):
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
            l.sort(reverse=reverse)
            for index, (_, k) in enumerate(l):
                self.tree.move(k, "", index)
            self.tree.heading(col, command=lambda: sort(col, not reverse))

    def records(self, from_where, to_where, departure_date, departure_time, flight_time, number_seats):
        self.db.insert_data(from_where, to_where, departure_date, departure_time, flight_time, number_seats)
        self.view_records()

    def update_record(self, from_where, to_where, departure_date, departure_time, flight_time):
        self.db.c.execute('''UPDATE route_table SET from_where=?, to_where=?, flight_time=? WHERE number=?''',
                          (from_where, to_where, flight_time, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.c.execute('''UPDATE departure_table SET departure_date=?, departure_time =? WHERE number=?''',
                          (departure_date, departure_time, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT route_table.number, route_table.from_where, route_table.to_where, 
                departure_table.departure_date, departure_table.departure_time, route_table.flight_time
        FROM route_table JOIN departure_table
        ON route_table.number = departure_table.number;''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM route_table WHERE number=?''', (self.tree.set(selection_item, '#1'),))
            self.db.c.execute('''DELETE FROM departure_table WHERE number=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, from_where, to_where, departure_date):
        from_where = str('%' + from_where + '%',)
        to_where = str('%' + to_where + '%',)
        departure_date = str('%' + departure_date + '%',)
        self.db.c.execute('''SELECT route_table.number, route_table.from_where, route_table.to_where, 
                departure_table.departure_date, departure_table.departure_time, route_table.flight_time
        FROM route_table JOIN departure_table
        ON route_table.number = departure_table.number 
        WHERE route_table.from_where LiKE ?
        AND route_table.to_where LiKE ?
        AND departure_table.departure_date LiKE ?''',
                          (from_where, to_where, departure_date))

        row = self.db.c.fetchone()
        if row is None:
            self.open_no_dialog()

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def open_seats_dialog(self):
        Seats()

    def open_no_dialog(self):
        No()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить рейс')
        self.geometry('400x320+400+300')
        self.resizable(False, False)


        label_from_where = tk.Label(self, text='Откуда:')
        label_from_where.place(x=50, y=50)
        label_to_where = tk.Label(self, text='Куда:')
        label_to_where.place(x=50, y=80)
        label_departure_date = tk.Label(self, text='Когда:')
        label_departure_date.place(x=50, y=110)
        label_departure_time = tk.Label(self, text='Во сколько:')
        label_departure_time.place(x=50, y=140)
        label_flight_time = tk.Label(self, text='Время в пути:')
        label_flight_time.place(x=50, y=170)
        label_number_seats = tk.Label(self, text='Количество мест:')
        label_number_seats.place(x=50, y=200)

        self.entry_from_where = ttk.Entry(self)
        self.entry_from_where.place(x=200, y=50)
        self.entry_to_where = ttk.Entry(self)
        self.entry_to_where.place(x=200, y=80)
        self.entry_departure_date = ttk.Entry(self)
        self.entry_departure_date.place(x=200, y=110)
        self.entry_departure_time = ttk.Entry(self)
        self.entry_departure_time.place(x=200, y=140)
        self.entry_flight_time = ttk.Entry(self)
        self.entry_flight_time.place(x=200, y=170)
        self.entry_number_seats = ttk.Entry(self)
        self.entry_number_seats.place(x=200, y=200)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=250)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=250)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_from_where.get(),
                                                                  self.entry_to_where.get(),
                                                                  self.entry_departure_date.get(),
                                                                  self.entry_departure_time.get(),
                                                                  self.entry_flight_time.get(),
                                                                  self.entry_number_seats.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать рейс')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=180, y=230)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_from_where.get(),
                                                                  self.entry_to_where.get(),
                                                                  self.entry_departure_date.get(),
                                                                  self.entry_departure_time.get(),
                                                                  self.entry_flight_time.get()))

        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM route_table WHERE number=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_from_where.insert(0, row[1])
        self.entry_to_where.insert(0, row[2])
        self.entry_flight_time.insert(0, row[3])
        self.db.c.execute('''SELECT * FROM departure_table WHERE number=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_departure_date.insert(0, row[1])
        self.entry_departure_time.insert(0, row[2])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x200+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Откуда')
        label_search.place(x=50, y=20)
        label_search = tk.Label(self, text='Куда')
        label_search.place(x=50, y=50)
        label_search = tk.Label(self, text='Когда')
        label_search.place(x=50, y=80)

        self.entry_search_from_where = ttk.Entry(self)
        self.entry_search_from_where.place(x=105, y=20, width=150)
        self.entry_search_to_where = ttk.Entry(self)
        self.entry_search_to_where.place(x=105, y=50, width=150)
        self.entry_search_date = ttk.Entry(self)
        self.entry_search_date.place(x=105, y=80, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=110)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=110)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search_from_where.get(),
                                                                             self.entry_search_to_where.get(),
                                                                             self.entry_search_date.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class Seats(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.db = db
        self.init_seats()

    def init_seats(self):
        self.title('Проверить количество мест')
        self.geometry('400x200+200+300')

        label_number = tk.Label(self, text='Введите номер рейса:')
        label_number.place(x=50, y=50)

        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=50)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=110)

        self.btn_check = ttk.Button(self, text='Проверить')
        self.btn_check.place(x=220, y=110)

        self.btn_check.bind('<Button-1>', lambda event: self.check(self.entry_number.get()))

    def check(self, number):
        for row in self.db.c.execute('''SELECT * FROM seats_table WHERE number LiKE ?''', number):
            label_number_seats = tk.Label(self, text=row[0])
            label_number_seats.place(x=180, y=80)

class No(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_no()

    def init_no(self):
        self.title('Ошибка')
        self.geometry('200x70+200+300')

        label_number = tk.Label(self, text='Нет подходящих запросов')
        label_number.place(x=20, y=20)


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('flight.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS route_table (number integer primary key, from_where text, to_where text, 
            flight_time text)''')
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS departure_table (number integer primary key, departure_date text, 
            departure_time text)''')
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS seats_table (number integer primary key, number_seats text)''')
        self.conn.commit()


    def insert_data(self, from_where, to_where, departure_date, departure_time, flight_time, number_seats):
        self.c.execute('''INSERT INTO route_table(from_where, to_where, flight_time) VALUES (?, ?, ?)''', (from_where,
                                                                                                           to_where,
                                                                                                           flight_time))
        self.c.execute('''INSERT INTO departure_table(departure_date, departure_time) VALUES (?, ?)''', (departure_date,
                                                                                                         departure_time))
        self.c.execute('''INSERT INTO seats_table(number_seats) VALUES (?)''', (number_seats,))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Система учета продаж")
    root.geometry("630x400+300+200")
    root.resizable(False, False)
    root.mainloop()
