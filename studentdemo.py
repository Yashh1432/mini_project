import re
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime


class studentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.config(bg="white")
        self.root.update_idletasks()
        self.center_window()
        self.root.focus_force()
        
            
        
        title = Label(self.root, text="Manage Student Details !!", padx=10, compound=LEFT, 
                      font=("goudy old style", 20, "bold"), bg="#B3E8E5", fg="black")
        title.place(x=0, y=0, relwidth=1, height=50)
        
        # Variables
        self.var_roll = StringVar(value="Autogenerated")
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        
        # Roll No
        lbl_roll = Label(self.root, text="Roll No", font=("goudy old style", 15, 'bold'), bg="white").place(x=10, y=70)
        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, 'bold'), 
                             bg="#e1f0f7", state="readonly")
        self.txt_roll.place(x=120, y=70, width=200)
        
        # Left Column Labels and Entries
        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 15, 'bold'), bg="white").place(x=10, y=130)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=120, y=130, width=200)
        
        lbl_email = Label(self.root, text="Email:", font=("goudy old style", 15, 'bold'), bg="white").place(x=10, y=190)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=120, y=190, width=200)
        
        lbl_gender = Label(self.root, text="Gender:", font=("goudy old style", 15, 'bold'), bg="white").place(x=10, y=250)
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), 
                                      font=("goudy old style", 15, 'bold'), state='readonly', justify=CENTER)
        self.txt_gender.place(x=120, y=250, width=200)
        self.txt_gender.current(0)
        
        lbl_state = Label(self.root, text="State:", font=("goudy old style", 15, 'bold'), bg="white").place(x=10, y=310)
        txt_state = Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=120, y=310, width=120)
        
        lbl_city = Label(self.root, text="City:", font=("goudy old style", 15, 'bold'), bg="white").place(x=270, y=310)
        txt_city = Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=340, y=310, width=120)
        
        lbl_pin = Label(self.root, text="Pin:", font=("goudy old style", 15, 'bold'), bg="white").place(x=490, y=310)
        txt_pin = Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=560, y=310, width=120)
        
        lbl_address = Label(self.root, text="Address:", font=("goudy old style", 15, 'bold'), bg="white").place(x=10, y=360)
        self.txt_address = Text(self.root, font=("goudy old style", 15, 'bold'), bg="#e1f0f7")
        self.txt_address.place(x=120, y=360, width=560, height=150)
        
        # Right Column Labels and Entries
        lbl_dob = Label(self.root, text="D.O.B:", font=("goudy old style", 15, 'bold'), bg="white").place(x=330, y=70)
        self.txt_dob = DateEntry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, 'bold'), 
                                bg="#e1f0f7", date_pattern='mm/dd/yyyy')  # Compatible format
        self.txt_dob.place(x=480, y=70, width=200)
        
        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15, 'bold'), bg="white").place(x=330, y=130)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=480, y=130, width=200)
        
        lbl_addmission = Label(self.root, text="Addmission:", font=("goudy old style", 15, 'bold'), bg="white").place(x=330, y=190)
        self.txt_a_date = DateEntry(self.root, textvariable=self.var_a_date, font=("goudy old style", 15, 'bold'), 
                                   bg="#e1f0f7", date_pattern='mm/dd/yyyy')  # Compatible format
        self.txt_a_date.place(x=480, y=190, width=200)
        
        lbl_course = Label(self.root, text="Course:", font=("goudy old style", 15, 'bold'), bg="white").place(x=330, y=250)
        self.course_list = []
        self.txt_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, 
                                      font=("goudy old style", 15, 'bold'), state='readonly', justify=CENTER)
        self.txt_course.place(x=480, y=250, width=200)
        self.txt_course.set("Select")
        self.fetch_course()
        
        # Buttons
        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, 'bold'), bg="#3BACB6", fg="black", 
                             cursor="hand2", command=self.add)
        self.btn_add.place(x=120, y=550, width=110, height=40)
        
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, 'bold'), bg="#B3E8E5", fg="black", 
                               cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=550, width=110, height=40)
        
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, 'bold'), bg="#3BACB6", fg="black", 
                               cursor="hand2", command=self.delete)
        self.btn_delete.place(x=420, y=550, width=110, height=40)
        
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, 'bold'), bg="#B3E8E5", fg="black", 
                              cursor="hand2", command=self.clear)
        self.btn_clear.place(x=570, y=550, width=110, height=40)
        
        # Search
        self.var_search = StringVar()
        lbl_search_roll = Label(self.root, text="Roll No:", font=("goudy old style", 15, 'bold'), bg="white").place(x=770, y=70)
        txt_search_roll = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, 'bold'), 
                               bg="#e1f0f7").place(x=890, y=70, width=390)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 12, 'bold'), bg="#3BACB6", fg="black", 
                           cursor="hand2", command=self.search).place(x=1305, y=70, width=120, height=30)
        
        # Course Table
        self.C_Frame = Frame(self.root, bd=10, relief=RIDGE)
        self.C_Frame.place(x=755, y=130, width=670, height=500)
        
        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "email", "gender", "dob", "contact", 
                                                              "admission", "course", "state", "city", "pin", "address"), 
                                       xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        self.CourseTable.heading("roll", text="Roll No")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("email", text="Email")
        self.CourseTable.heading("gender", text="Gender")
        self.CourseTable.heading("dob", text="D.O.B")
        self.CourseTable.heading("contact", text="Contact")
        self.CourseTable.heading("admission", text="Admission")
        self.CourseTable.heading("course", text="Course")
        self.CourseTable.heading("state", text="State")
        self.CourseTable.heading("city", text="City")
        self.CourseTable.heading("pin", text="PIN")
        self.CourseTable.heading("address", text="Address")
        
        self.CourseTable["show"] = 'headings'
        self.CourseTable.column("roll", width=100)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("email", width=100)
        self.CourseTable.column("gender", width=100)
        self.CourseTable.column("dob", width=100)
        self.CourseTable.column("contact", width=100)
        self.CourseTable.column("admission", width=100)
        self.CourseTable.column("course", width=100)
        self.CourseTable.column("state", width=100)
        self.CourseTable.column("city", width=100)
        self.CourseTable.column("pin", width=100)
        self.CourseTable.column("address", width=100)
        
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        
        footer = Label(self.root, text="Student Management System | GUJJU infotech | Contact Us: 7874273210",
                       font=("goudy old style", 12),  bg="#2F8F9D", fg="black")
        footer.pack(side=BOTTOM, fill=X)
        
        
        
        
        
        
        
    def clear(self):
        self.show()
        self.var_roll.set("Auto generated")  # Reset to Autogenerated
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")  # Reset to default
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_a_date.set("")
        self.var_course.set("Select")  # Reset to default
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)
        self.var_search.set("")

    def delete(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            if not self.var_roll.get() or self.var_roll.get() == "Autogenerated":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Please select a student from the list first", parent=self.root)
                return
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op:
                cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Student Deleted Successfully", parent=self.root)
                self.clear()
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    def get_data(self, ev):
        self.txt_roll.config(state="normal")
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        if row:
            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            dob = row[4]
            if dob and '-' in dob:
                dob = datetime.strptime(dob, '%Y-%m-%d').strftime('%m/%d/%Y')  # Match DateEntry format
            self.var_dob.set(dob)
            self.var_contact.set(row[5])
            admission = row[6]
            if admission and '-' in admission:
                admission = datetime.strptime(admission, '%Y-%m-%d').strftime('%m/%d/%Y')  # Match DateEntry format
            self.var_a_date.set(admission)
            self.var_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(str(row[10]) if row[10] is not None else "")
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[11])
        self.txt_roll.config(state="readonly")

    def parse_date(self, date_str, field_name):
        if not date_str.strip():
            messagebox.showerror("Error", f"{field_name} is required", parent=self.root)
            return None
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            try:
                # Fallback for two-digit years (e.g., '3/27/03' -> '2003-03-27')
                return datetime.strptime(date_str, '%m/%d/%y').replace(year=date_str[-2:] > '50' and 1900 or 2000 + int(date_str[-2:])).strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", f"Invalid {field_name} format. Use MM/DD/YYYY (e.g., 03/18/2025), got {date_str}")
                return None

    def add(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            
            if not self.validate_all():
                return
            
            cur.execute("SELECT name FROM course WHERE name=?", (self.var_course.get(),))
            if cur.fetchone() is None:
                messagebox.showerror("Error", "Selected course does not exist", parent=self.root)
                return
            
            dob = self.parse_date(self.var_dob.get(), "Date of Birth")
            if dob is None:
                return
            admission = self.parse_date(self.var_a_date.get(), "Admission Date")
            if admission is None:
                return
            
            pin = int(self.var_pin.get()) if self.var_pin.get().strip() else None
            
            cur.execute("""
                INSERT INTO student (name, email, gender, dob, contact, admission, course, state, city, pin, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                dob,
                self.var_contact.get(),
                admission,
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                pin,
                self.txt_address.get("1.0", END).strip()
            ))
            
            con.commit()
            if cur.rowcount > 0:
                cur.execute("SELECT last_insert_rowid()")
                last_roll = cur.fetchone()[0]
                self.var_roll.set(str(last_roll))
                messagebox.showinfo("Success", f"Student Added Successfully with Roll No: {last_roll}", parent=self.root)
                self.show()
                self.clear()  # Uncomment to reset all fields
            else:
                messagebox.showerror("Error", "Failed to insert student", parent=self.root)
                    
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()
                

    def update(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            if not self.var_roll.get() or self.var_roll.get() == "Autogenerated":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Select a student from the list", parent=self.root)
                return
            if not self.validate_all():
                return
            
            cur.execute("SELECT name FROM course WHERE name=?", (self.var_course.get(),))
            if cur.fetchone() is None:
                messagebox.showerror("Error", "Selected course does not exist", parent=self.root)
                return
            
            dob = self.parse_date(self.var_dob.get(), "Date of Birth")
            if dob is None:
                return
            admission = self.parse_date(self.var_a_date.get(), "Admission Date")
            if admission is None:
                return
            
            pin = int(self.var_pin.get()) if self.var_pin.get().strip() else None
                
            cur.execute("""
                UPDATE student 
                SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, 
                    state=?, city=?, pin=?, address=?
                WHERE roll=?
            """, (
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                dob,
                self.var_contact.get(),
                admission,
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                pin,
                self.txt_address.get("1.0", END).strip(),
                self.var_roll.get()
            ))
            
            con.commit()
            if cur.rowcount > 0:
                messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
                self.show()
                self.clear()
            else:
                messagebox.showerror("Error", "No changes were made", parent=self.root)
                
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        except ValueError as ex:
            messagebox.showerror("Error", f"Date or PIN format error: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    def search(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            self.CourseTable.delete(*self.CourseTable.get_children())
            if row:
                self.CourseTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No Record Found", parent=self.root)
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    def show(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    def fetch_course(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.course_list = [row[0] for row in rows] if rows else ["No courses available"]
            self.txt_course['values'] = self.course_list
            if self.var_course.get() not in self.course_list:
                self.txt_course.set("Select")
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Error fetching courses: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    def center_window(self, width=1450, height=700):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_contact(self, contact):
        return contact.isdigit() and len(contact) == 10

    def validate_pin(self, pin):
        return pin.isdigit() and len(pin) == 6

    def validate_required_fields(self):
        required_fields = {
            "Name": self.var_name.get(),
            "Email": self.var_email.get(),
            "Contact": self.var_contact.get(),
            "Gender": self.var_gender.get(),
            "Course": self.var_course.get()
        }
        for field_name, value in required_fields.items():
            if not value.strip():
                messagebox.showerror("Error", f"{field_name} is required", parent=self.root)
                return False
            if field_name == "Gender" and value == "Select":
                messagebox.showerror("Error", "Please select a valid Gender", parent=self.root)
                return False
            if field_name == "Course" and value == "Select":
                messagebox.showerror("Error", "Please select a valid Course", parent=self.root)
                return False
        return True

    def validate_state_city(self, value, field_name):
        """Check if state or city is non-empty and not an integer."""
        stripped_value = value.strip()
        if not stripped_value:
            return True  # Optional field
        if stripped_value.isdigit():
            messagebox.showerror("Error", f"{field_name} must not be a number", parent=self.root)
            return False
        if len(stripped_value) > 50:  # Optional: limit length
            messagebox.showerror("Error", f"{field_name} must be 50 characters or less", parent=self.root)
            return False
        return True

    def validate_all(self):
        if not self.validate_required_fields():
            return False
        if not self.validate_email(self.var_email.get()):
            messagebox.showerror("Error", "Invalid Email format", parent=self.root)
            return False
        if not self.validate_contact(self.var_contact.get()):
            messagebox.showerror("Error", "Contact must be a 10-digit number", parent=self.root)
            return False
        if self.var_pin.get() and not self.validate_pin(self.var_pin.get()):
            messagebox.showerror("Error", "PIN must be a 6-digit number", parent=self.root)
            return False
        if not self.validate_state_city(self.var_state.get(), "State"):
            return False
        if not self.validate_state_city(self.var_city.get(), "City"):
            return False
        return True

if __name__ == "__main__":
    root = Tk()
    obj = studentClass(root)
    root.mainloop()