import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="",  # Change to your MySQL username
        password="",  # Change to your MySQL password
        database="student_db"
    )

# Add student
def add_student():
    name = name_var.get()
    age = age_var.get()
    course = course_var.get()
    if name and age and course:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO students (name, age, course) VALUES (%s, %s, %s)", (name, age, course))
        db.commit()
        db.close()
        fetch_students()
        clear_form()
        messagebox.showinfo("Success", "Student added successfully")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update student
def update_student():
    if selected_id.get():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s", 
                       (name_var.get(), age_var.get(), course_var.get(), selected_id.get()))
        db.commit()
        db.close()
        fetch_students()
        clear_form()
        messagebox.showinfo("Success", "Student updated successfully")
    else:
        messagebox.showwarning("Selection Error", "Please select a student to update")

# Delete student
def delete_student():
    if selected_id.get():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (selected_id.get(),))
        db.commit()
        db.close()
        fetch_students()
        clear_form()
        messagebox.showinfo("Success", "Student deleted successfully")
    else:
        messagebox.showwarning("Selection Error", "Please select a student to delete")

# Fetch students
def fetch_students():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    db.close()
    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", "end", values=row)

# Select student from table
def select_student(event):
    selected = student_table.focus()
    if selected:
        values = student_table.item(selected, 'values')
        selected_id.set(values[0])
        name_var.set(values[1])
        age_var.set(values[2])
        course_var.set(values[3])

# Clear form
def clear_form():
    selected_id.set("")
    name_var.set("")
    age_var.set("")
    course_var.set("")

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("600x500")

selected_id = tk.StringVar()
name_var = tk.StringVar()
age_var = tk.StringVar()
course_var = tk.StringVar()

# Form
tk.Label(root, text="Name").pack()
tk.Entry(root, textvariable=name_var).pack()

tk.Label(root, text="Age").pack()
tk.Entry(root, textvariable=age_var).pack()

tk.Label(root, text="Course").pack()
tk.Entry(root, textvariable=course_var).pack()

tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="Update Student", command=update_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)
tk.Button(root, text="Clear Form", command=clear_form).pack(pady=5)

# Table
student_table = ttk.Treeview(root, columns=("ID", "Name", "Age", "Course"), show="headings")
student_table.heading("ID", text="ID")
student_table.heading("Name", text="Name")
student_table.heading("Age", text="Age")
student_table.heading("Course", text="Course")
student_table.pack(fill="both", expand=True)
student_table.bind("<ButtonRelease-1>", select_student)

fetch_students()

root.mainloop()
