import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

conn = sqlite3.connect('hospital_management.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    diagnosis TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    address TEXT NOT NULL,
                    admission_date TEXT NOT NULL)''')
conn.commit()


def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    diagnosis = entry_diagnosis.get()
    contact = entry_contact.get()
    address = entry_address.get()
    admission_date = entry_admission_date.get()

    if not all([name, age, gender, diagnosis, contact, address, admission_date]):
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        
        age = int(age)
        if age <= 0:
            raise ValueError("Age must be a positive number")
        
        datetime.strptime(admission_date, '%Y-%m-%d')
    except ValueError as ve:
        messagebox.showerror("Validation Error", str(ve))
        return

    try:
        cursor.execute(
            "INSERT INTO patients (name, age, gender, diagnosis, contact, address, admission_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, age, gender, diagnosis, contact, address, admission_date)
        )
        conn.commit()
        messagebox.showinfo("Success", "Patient record added successfully")
        clear_fields()
    except sqlite3.Error as db_error:
        messagebox.showerror("Database Error", str(db_error))



def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_diagnosis.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_admission_date.delete(0, tk.END)


def view_patient_records():
    view_window = tk.Toplevel(root)
    view_window.title("View Patient Records")

    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()

    columns = ["Patient ID", "Name", "Age", "Gender", "Diagnosis", "Contact", "Address", "Admission Date"]

    tree = ttk.Treeview(view_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    for record in records:
        tree.insert('', tk.END, values=record)

    tree.pack(fill=tk.BOTH, expand=True)
    ttk.Button(view_window, text="Close", command=view_window.destroy).pack(pady=10)


def update_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_day = datetime.now().strftime('%A')
    time_label.config(text=f"{current_time} | {current_day}")
    root.after(1000, update_time)


root = tk.Tk()
root.title("Hospital Management System")
root.geometry("800x600")
root.configure(bg="#f0f8ff")


frame = ttk.LabelFrame(root, text="Patient Details", padding=(20, 10))
frame.pack(pady=20, padx=20, fill="both")


ttks = ttk.Style()
ttks.configure("TLabel", font=("Helvetica", 10))
ttks.configure("TEntry", font=("Helvetica", 10))

ttk.Label(frame, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = ttk.Entry(frame, width=40)
entry_name.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame, text="Age:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_age = ttk.Entry(frame, width=40)
entry_age.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame, text="Gender:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
gender_var = tk.StringVar(value="Male")
ttk.Radiobutton(frame, text="Male", variable=gender_var, value="Male").grid(row=2, column=1, padx=5, sticky="w")
ttk.Radiobutton(frame, text="Female", variable=gender_var, value="Female").grid(row=2, column=2, padx=5, sticky="w")

ttk.Label(frame, text="Diagnosis:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_diagnosis = ttk.Entry(frame, width=40)
entry_diagnosis.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(frame, text="Contact:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_contact = ttk.Entry(frame, width=40)
entry_contact.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(frame, text="Address:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
entry_address = ttk.Entry(frame, width=40)
entry_address.grid(row=5, column=1, padx=10, pady=5)

ttk.Label(frame, text="Admission Date (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
entry_admission_date = ttk.Entry(frame, width=40)
entry_admission_date.grid(row=6, column=1, padx=10, pady=5)


btn_frame = ttk.Frame(frame)
btn_frame.grid(row=7, column=0, columnspan=3, pady=10)

ttk.Button(btn_frame, text="Add Patient", command=add_patient).pack(side="left", padx=10)

ttk.Button(btn_frame, text="View Records", command=view_patient_records).pack(side="left", padx=10)


time_label = ttk.Label(root, font=('Helvetica', 10), anchor='e', background="#f0f8ff")
time_label.pack(fill=tk.X, pady=5)

update_time()
root.mainloop()

conn.close()
