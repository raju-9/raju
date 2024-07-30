import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database setup
conn = sqlite3.connect('student_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        name varchar(10),
        uucms varchar(12),
        gender varchar(10),
        course varchar(10),
        semester varchar(10),
        password varchar(10),
        PRIMARY KEY(uucms)
    )
''')
conn.commit()


# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Function to register student details
def register():
    name = name_entry.get()
    student_id = id_entry.get()
    gender = gender_var.get()
    course = course_dropdown.get()
    semester = sem_dropdown.get()
    password = password_entry.get()

    if not all([name, student_id, gender, course, semester, password]):
        messagebox.showwarning("Incomplete Data", "Please fill out all fields.")
        return

    try:
        cursor.execute('''
            INSERT INTO students (name, uucms, gender, course, semester, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, student_id, gender, course, semester, password))
        conn.commit()
        messagebox.showinfo("Registration", "Registration Successful")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists")

# Function to show student details
def display_details():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
   
    treeview = ttk.Treeview(form, columns=("name", "uucms", "gender","course", "semester", "password"), show='headings')
    treeview.heading("name", text="name")
    treeview.heading("uucms", text="uucms")
    treeview.heading("gender", text="gender")
    treeview.heading("course", text="course")
    treeview.heading("semester", text="semester")
    treeview.heading("password", text="password")

    for row in rows:
        treeview.insert("", "end", values=row)
    treeview.grid(row=16,column=0)

# Function to login
def login():
    student_id = login_id_entry.get()
    password = login_password_entry.get()
   
    cursor.execute('SELECT * FROM students WHERE uucms = ? AND password = ?', (student_id, password))
    student = cursor.fetchone()
   
    if student:
        messagebox.showinfo("Login", "Login Successful")
    else:
        messagebox.showerror("Login", "Invalid ID or Password")

# Initialize main window
form = tk.Tk()
form.title("Student Management System")
form.geometry("500x500")

# Create frames
login_frame = tk.Frame(form)
register_frame = tk.Frame(form)

for frame in (login_frame,register_frame):
    frame.grid(row=0,column=0,sticky='nsew')
    

# Login Frame
lbluucms=tk.Label(login_frame, text="U15IG22S0206",fg='red', font=('Times New Roman', 20, 'bold'))
lbluucms.grid(row=1,column=1,sticky=tk.W,padx=10,pady=2)
lbllogin=tk.Label(login_frame, text="Login Page", font=('Times New Roman', 18, 'bold'))
lbllogin.grid(row=2,column=0,sticky=tk.W,padx=10,pady=10)

lblid=tk.Label(login_frame, text="UUCMS No")
lblid.grid(row=3,column=0,sticky=tk.W,padx=10,pady=10)
login_id_entry = tk.Entry(login_frame)
login_id_entry.grid(row=3,column=1,sticky=tk.W,padx=10,pady=5)

lblpwd=tk.Label(login_frame, text="Password")
lblpwd.grid(row=4,column=0,sticky=tk.W,padx=10,pady=10)
login_password_entry = tk.Entry(login_frame, show='*')
login_password_entry.grid(row=4,column=1,sticky=tk.W,padx=10,pady=10)

btnlog=tk.Button(login_frame, text="Login", command=login)
btnlog.grid(row=5,column=0,sticky=tk.W,padx=10,pady=10)
btnreg=tk.Button(login_frame, text="Register", command=lambda: show_frame(register_frame))
btnreg.grid(row=5,column=1,sticky=tk.W,padx=10,pady=10)

# Register Frame
lblregpage=tk.Label(register_frame, text="Registration Page", font=('Times New Roman', 18, 'bold'))
lblregpage.grid(row=6,column=1,sticky=tk.W,padx=10,pady=10)

lblregpage=tk.Label(register_frame, text="U15IG22S0206", fg="RED",font=('Times New Roman', 18, 'bold'))
lblregpage.grid(row=7,column=1,sticky=tk.W,padx=10,pady=10)

lblname=tk.Label(register_frame, text="Name")
lblname.grid(row=8,column=1,sticky=tk.W,padx=10,pady=10)
name_entry = tk.Entry(register_frame)
name_entry.grid(row=8,column=2,sticky=tk.W,padx=10,pady=10)

id=tk.Label(register_frame, text="UUCMS No")
id.grid(row=9,column=1,sticky=tk.W,padx=10,pady=10)
id_entry = tk.Entry(register_frame)
id_entry.grid(row=9,column=2,sticky=tk.W,padx=10,pady=10)

lblgen=tk.Label(register_frame, text="Gender")
lblgen.grid(row=10,column=1,sticky=tk.W,padx=10,pady=10)
gender_var = tk.StringVar(value="Male")
rdbtn=tk.Radiobutton(register_frame, text="Male", variable=gender_var, value="Male")
rdbtn.grid(row=10,column=2,sticky=tk.W,padx=10,pady=2)
rdbtnfe=tk.Radiobutton(register_frame, text="Female", variable=gender_var, value="Female")
rdbtnfe.grid(row=10,column=3,sticky=tk.W,padx=10,pady=2)

choices=["BCA","BBA","B.COM","BA"]
lblcor=tk.Label(register_frame, text="Course")
lblcor.grid(row=11,column=1,sticky=tk.W,padx=10,pady=10)
course_dropdown= ttk.Combobox(register_frame,values=choices)
course_dropdown.grid(row=11,column=2,sticky=tk.W,padx=10,pady=10)

semister=["I","II","III","IV","V","VI"]
lblsem=tk.Label(register_frame, text="Semester")
lblsem.grid(row=12,column=1,sticky=tk.W,padx=10,pady=10)
sem_dropdown = ttk.Combobox(register_frame,values=semister)
sem_dropdown.grid(row=12,column=2,sticky=tk.W,padx=10,pady=10)

lblpwd=tk.Label(register_frame, text="Password")
lblpwd.grid(row=13,column=1,sticky=tk.W,padx=10,pady=10)
password_entry = tk.Entry(register_frame, show='*')
password_entry.grid(row=13,column=2,sticky=tk.W,padx=10,pady=10)

btn=tk.Button(register_frame, text="Register", command=register)
btn.grid(row=14,column=1,sticky=tk.W,padx=10,pady=10)
btndisp=tk.Button(register_frame, text="Show Details", command=display_details)
btndisp.grid(row=14,column=2,sticky=tk.W,padx=10,pady=10)
btnlg=tk.Button(register_frame, text="Back to Login", command=lambda: show_frame(login_frame))
btnlg.grid(row=15,column=1,sticky=tk.W,padx=10,pady=10)

# Show login frame initially
show_frame(login_frame)

# Run the application
form.mainloop()

# Close the database connection when the application is closed
conn.close()