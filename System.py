import sqlite3
import tkinter as tk
from tkinter import ttk , messagebox

class OrderDashBoard():
    def __init__(self , db_name = "orders.db"):
        self.db_name = db_name
    
    def connect_db(self):
        return sqlite3.connect(self.db_name)
    
    def Table(self):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
                       id INTEGER PRIMARY KEY AUTOINCREMENT ,
                       customer_name TEXT,
                       amount REAL,
                       order_date TEXT)""")
        
        conn.commit()
        conn.close()

    def Insert_record(self , customer_name , amount , order_date):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO orders (customer_name , amount , order_date) VALUES (?,?,?)""",
        (customer_name , amount , order_date ))

        conn.commit()
        conn.close()

    def View_record(self):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        return orders
    
    def delete_record(self , record_id):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM orders WHERE id = ? ", (record_id,))

        conn.commit()
        conn.close()

    

class App:
    def __init__(self, root):
        self.db = OrderDashBoard()
        self.db.Table()

        self.root = root
        self.root.title("Orders")
        self.root.geometry("800x800")

        frame = tk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Label(frame, text="Amount").grid(row=1, column=0)
        tk.Label(frame, text="Date").grid(row=2, column=0)

        self.name = tk.Entry(frame)
        self.amount = tk.Entry(frame)
        self.date = tk.Entry(frame)

        self.name.grid(row=0, column=1)
        self.amount.grid(row=1, column=1)
        self.date.grid(row=2, column=1)

        tk.Button(frame, text="Add", command=self.add).grid(row=3, column=0)
        tk.Button(frame, text="Show", command=self.show).grid(row=3, column=1)
        tk.Button (frame, text="Delete", command=self.delete).grid(row =3 , column=2)

        self.listbox = tk.Listbox(frame, width=40)
        self.listbox.grid(row=4, column=0, columnspan=2)

    def add(self):
        self.db.Insert_record(
            self.name.get(),
            float(self.amount.get()),
            self.date.get()
        )

    def show(self):
        self.listbox.delete(0, tk.END)
        for row in self.db.View_record():
            self.listbox.insert(tk.END, row)

    def delete(self):
        selected = self.listbox.curselection()

        if not selected:
            from tkinter import messagebox
            messagebox.showwarning("Error", "Select a record")
            return
        
        record = self.listbox.get(selected[0])
        record_id = record[0]

        self.db.delete_record(record_id)

        self.show()

        from tkinter import messagebox
        messagebox.showwarning("Deleted" ,"record deleted succesfully")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()