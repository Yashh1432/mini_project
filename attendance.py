import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import csv
from calendar import monthrange
# from Login import Login
# from Register import Register





class AttendanceClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.config(bg="#F5F7FA")
        self.root.geometry("1200x650")
        self.root.update_idletasks()
        self.center_window()
        self.root.focus_force()
        
        
    # #     # Start with Register window
    #     self.show_login()

    # def show_register(self):
    #     print("Opening Register Page")  # Debug
    #     for widget in self.root.winfo_children():   
    #         widget.destroy()
    #     Register(self.root, self.show_login)

    # def show_login(self):
    #     print("Opening Login Page")  # Debug
    #     for widget in self.root.winfo_children():
    #         widget.destroy()
    #     # Pass the dashboard callback as a lambda to ensure proper binding
    #     Login(self.root, lambda: self.show_dashboard())

    # def show_dashboard(self):
    #     print("Opening Dashboard")  # Debug
    #     for widget in self.root.winfo_children():
    #         widget.destroy()
            

        # Title Frame
        title_frame = Frame(self.root, bg="#4A90E2", relief=RIDGE, bd=2)
        title_frame.place(x=0, y=0, relwidth=1, height=60)
        title = Label(title_frame, text="Student Attendance Management", padx=20,
                      font=("goudy old style", 24, "bold"), bg="#4A90E2", fg="white")
        title.pack(anchor="w", pady=10)

        # Main Frame for Inputs
        input_frame = Frame(self.root, bg="#F5F7FA", relief=RIDGE, bd=2)
        input_frame.place(x=20, y=70, width=1160, height=80)

        lbl_select_course = Label(input_frame, text="Select Course:", font=("goudy old style", 14, "bold"), bg="#F5F7FA")
        lbl_select_course.place(x=20, y=25)
        self.var_course = StringVar()
        self.course_list = []
        self.txt_course = ttk.Combobox(input_frame, textvariable=self.var_course, values=self.course_list,
                                      font=("goudy old style", 12), state='readonly', justify=CENTER)
        self.txt_course.place(x=200, y=25, width=200)
        self.txt_course.set("Select")
        self.txt_course.bind("<<ComboboxSelected>>", self.update_student_list)

        lbl_date = Label(input_frame, text="Date:", font=("goudy old style", 15, "bold"), bg="#F5F7FA")
        lbl_date.place(x=500, y=25)
        self.date = StringVar()
        self.cal = DateEntry(input_frame, textvariable=self.date, date_pattern='yyyy-mm-dd',
                            font=("goudy old style", 12), bg="#e1f0f7")
        self.cal.place(x=590, y=25, width=200)
        
        self.btn_report = Button(input_frame, text="Attendance Report", font=("goudy old style", 15),
                                bg="#007BFF", fg="white", command=self.generate_attendance_report)
        self.btn_report.place(x=830, y=25, width=170, height=40)
        self.btn_report.bind("<Enter>", lambda e: self.btn_report.config(bg="#0056b3"))
        self.btn_report.bind("<Leave>", lambda e: self.btn_report.config(bg="#007BFF"))

        # Frame for Student List
        self.student_frame = Frame(self.root, bd=0, relief=FLAT, bg="#FFFFFF")
        self.student_frame.place(x=20, y=160, width=1160, height=400)

        # Header for Student List
        header_frame = Frame(self.student_frame, bg="#2C3E50", bd=0, relief=FLAT)
        header_frame.pack(fill=X)
        Label(header_frame, text="Roll", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=10).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Name", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=15).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Email", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=20).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Gender", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=10).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Status", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=20).pack(side=LEFT, padx=10, pady=5)

        # Canvas for Scrollable Student List
        self.canvas = Canvas(self.student_frame, bg="#FFFFFF")
        scrollbar = Scrollbar(self.student_frame, orient=VERTICAL, command=self.canvas.yview)
        self.inner_frame = Frame(self.canvas, bg="#FFFFFF")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Fetch courses
        self.student_data = {}
        self.fetch_courses()

        # Button Frame
        button_frame = Frame(self.root, bg="#F5F7FA")
        button_frame.place(x=20, y=570, width=1160, height=50)

        self.btn_submit = Button(button_frame, text="Submit Attendance", font=("goudy old style", 14, "bold"),
                                bg="#28A745", fg="white", command=self.submit_attendance)
        self.btn_submit.place(x=0, y=5, width=200, height=40)
        self.btn_submit.bind("<Enter>", lambda e: self.btn_submit.config(bg="#218838"))
        self.btn_submit.bind("<Leave>", lambda e: self.btn_submit.config(bg="#28A745"))

        self.btn_clear = Button(button_frame, text="Clear", font=("goudy old style", 14, "bold"),
                               bg="#DC3545", fg="white", command=self.clear)
        self.btn_clear.place(x=220, y=5, width=200, height=40)
        self.btn_clear.bind("<Enter>", lambda e: self.btn_clear.config(bg="#C82333"))
        self.btn_clear.bind("<Leave>", lambda e: self.btn_clear.config(bg="#DC3545"))

        self.btn_all_present = Button(button_frame, text="All Present", font=("goudy old style", 14),
                                     bg="#17A2B8", fg="white", command=self.set_all_present)
        self.btn_all_present.place(x=440, y=5, width=120, height=40)
        self.btn_all_present.bind("<Enter>", lambda e: self.btn_all_present.config(bg="#138496"))
        self.btn_all_present.bind("<Leave>", lambda e: self.btn_all_present.config(bg="#17A2B8"))

        self.btn_all_absent = Button(button_frame, text="All Absent", font=("goudy old style", 14),
                                    bg="#FFC107", fg="black", command=self.set_all_absent)
        self.btn_all_absent.place(x=570, y=5, width=120, height=40)
        self.btn_all_absent.bind("<Enter>", lambda e: self.btn_all_absent.config(bg="#E0A800"))
        self.btn_all_absent.bind("<Leave>", lambda e: self.btn_all_absent.config(bg="#FFC107"))

        self.btn_view = Button(button_frame, text="View Attendance", font=("goudy old style", 14),
                              bg="#6C757D", fg="white", command=self.view_attendance)
        self.btn_view.place(x=700, y=5, width=150, height=40)
        self.btn_view.bind("<Enter>", lambda e: self.btn_view.config(bg="#5A6268"))
        self.btn_view.bind("<Leave>", lambda e: self.btn_view.config(bg="#6C757D"))


        self.lbl_present = Label(button_frame, text="Present: 0", font=("goudy old style", 14, "bold"), bg="#F5F7FA", fg="#28A745")
        self.lbl_present.place(x=980, y=10)
        self.lbl_absent = Label(button_frame, text="Absent: 0", font=("goudy old style", 14, "bold"), bg="#F5F7FA", fg="#DC3545")
        self.lbl_absent.place(x=1080, y=10)

        # Footer
        footer = Label(self.root, text="Student Management System | GUJJU infotech | Contact Us: 7874273210",
                       font=("goudy old style", 12), bg="#2F8F9D", fg="black")
        footer.pack(side=BOTTOM, fill=X)

    def fetch_courses(self):
        con = sqlite3.connect(database="sms.db")
        cur = con.cursor()
        try:
            self.course_list.clear()
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.course_list.append(row[0])
            self.txt_course['values'] = self.course_list
            if not self.course_list:
                messagebox.showwarning("Warning", "No courses found in the database. Please add courses first.")
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Error fetching courses: {str(ex)}")
        finally:
            con.close()

    def update_student_list(self, event):
        selected_course = self.var_course.get()
        if selected_course != "Select":
            self.inner_frame.destroy()
            self.inner_frame = Frame(self.canvas, bg="#FFFFFF")
            self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
            self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            try:
                self.student_data.clear()
                cur.execute("SELECT roll, name, email, gender FROM student WHERE LOWER(course) = LOWER(?)", (selected_course,))
                rows = cur.fetchall()
                if len(rows) > 0:
                    for idx, (roll, name, email, gender) in enumerate(rows):
                        self.student_data[roll] = {'name': name, 'email': email, 'gender': gender, 'status': StringVar(value='A')}
                        frame = Frame(self.inner_frame, bg="#FFFFFF" if idx % 2 == 0 else "#F5F5F5", bd=0, relief=FLAT)
                        frame.pack(fill=X, pady=10)
                        frame.bind("<Enter>", lambda e, f=frame: f.config(bg="#E0E0E0"))
                        frame.bind("<Leave>", lambda e, f=frame, i=idx: f.config(bg="#FFFFFF" if i % 2 == 0 else "#F5F5F5"))

                        Label(frame, text=str(roll), font=("goudy old style", 12), bg=frame.cget("bg"), width=10).pack(side=LEFT, padx=10, pady=5)
                        Label(frame, text=name, font=("goudy old style", 12), bg=frame.cget("bg"), width=15).pack(side=LEFT, padx=10, pady=5)
                        Label(frame, text=email, font=("goudy old style", 12), bg=frame.cget("bg"), width=20).pack(side=LEFT, padx=10, pady=5)
                        Label(frame, text=gender, font=("goudy old style", 12), bg=frame.cget("bg"), width=10).pack(side=LEFT, padx=10, pady=5)

                        status_frame = Frame(frame, bg=frame.cget("bg"), bd=0, relief=FLAT)
                        status_frame.pack(side=LEFT, padx=10, pady=5)

                        present_radio = Radiobutton(status_frame, text="Present", variable=self.student_data[roll]['status'], value='P',
                                                   font=("goudy old style", 12, "bold"), bg=frame.cget("bg"), fg="#28A745",
                                                   selectcolor="#D4F1DE", indicatoron=1, width=8, padx=5, pady=5)
                        present_radio.pack(side=LEFT, padx=5)
                        absent_radio = Radiobutton(status_frame, text="Absent", variable=self.student_data[roll]['status'], value='A',
                                                  font=("goudy old style", 12, "bold"), bg=frame.cget("bg"), fg="#DC3545",
                                                  selectcolor="#FAD2D2", indicatoron=1, width=8, padx=5, pady=5)
                        absent_radio.pack(side=LEFT, padx=5)
                else:
                    Label(self.inner_frame, text="No students enrolled in this course.", font=("goudy old style", 12), bg="#FFFFFF").pack(pady=10)

                if len(rows) < 5:
                    for _ in range(5 - len(rows)):
                        frame = Frame(self.inner_frame, bg="#FFFFFF", bd=0, relief=FLAT)
                        frame.pack(fill=X, pady=10)
                        Label(frame, text="", font=("goudy old style", 12), bg=frame.cget("bg"), width=10).pack(side=LEFT, padx=10, pady=5)
                        Label(frame, text="No more students", font=("goudy old style", 12), bg=frame.cget("bg"), width=15, fg="#6C757D").pack(side=LEFT, padx=10, pady=5)
                        Label(frame, text="", font=("goudy old style", 12), bg=frame.cget("bg"), width=20).pack(side=LEFT, padx=10, pady=5)
                        Label(frame, text="", font=("goudy old style", 12), bg=frame.cget("bg"), width=10).pack(side=LEFT, padx=10, pady=5)
                        status_frame = Frame(frame, bg=frame.cget("bg"), bd=0, relief=FLAT)
                        status_frame.pack(side=LEFT, padx=10, pady=5)

                self.canvas.config(height=300)
            except sqlite3.Error as ex:
                messagebox.showerror("Error", f"Error fetching students: {str(ex)}")
            finally:
                con.close()
        else:
            self.inner_frame.destroy()
            self.inner_frame = Frame(self.canvas, bg="#FFFFFF")
            self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
            self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            Label(self.inner_frame, text="Please select a course.", font=("goudy old style", 12), bg="#FFFFFF").pack(pady=10)

    def set_all_present(self):
        for roll, data in self.student_data.items():
            data['status'].set('P')
        messagebox.showinfo("Success", "All students marked as Present.", parent=self.root)

    def set_all_absent(self):
        for roll, data in self.student_data.items():
            data['status'].set('A')
        messagebox.showinfo("Success", "All students marked as Absent.", parent=self.root)

    def submit_attendance(self):
        if self.var_course.get() == "Select":
            messagebox.showerror("Error", "Please select a course", parent=self.root)
            return
        try:
            datetime.strptime(self.date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.", parent=self.root)
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to submit attendance?", parent=self.root):
            return

        con = sqlite3.connect(database="sms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT cid FROM course WHERE name=?", (self.var_course.get(),))
            course_id = cur.fetchone()
            if not course_id:
                messagebox.showerror("Error", "Invalid course", parent=self.root)
                return
            course_id = course_id[0]

            present_count = 0
            absent_count = 0
            for roll, data in self.student_data.items():
                status = data['status'].get()
                cur.execute("INSERT OR REPLACE INTO attendance (roll, date, course, status) VALUES (?, ?, ?, ?)",
                           (roll, self.date.get(), course_id, status))
                if status == 'P':
                    present_count += 1
                else:
                    absent_count += 1

            con.commit()
            self.lbl_present.config(text=f"Present: {present_count}")
            self.lbl_absent.config(text=f"Absent: {absent_count}")
            messagebox.showinfo("Success", "Attendance Submitted Successfully", parent=self.root)
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Error submitting attendance: {str(ex)}")
        finally:
            con.close()

    def view_attendance(self):
        if self.var_course.get() == "Select":
            messagebox.showerror("Error", "Please select a course", parent=self.root)
            return

        view_window = Toplevel(self.root)
        view_window.title("Attendance Report")
        view_window.geometry("800x500")
        self.center_window(view_window, 800, 500)
        view_window.config(bg="#F5F7FA")

        title_frame = Frame(view_window, bg="#4A90E2", relief=RIDGE, bd=2)
        title_frame.pack(fill=X, pady=10)
        Label(title_frame, text="Attendance Report for ", font=("goudy old style", 16, "bold"), bg="#4A90E2", fg="white").pack(side=LEFT, padx=10)
        self.view_date = StringVar(value=self.date.get() if self.date.get() else datetime.now().strftime("%Y-%m-%d"))
        view_cal = DateEntry(title_frame, textvariable=self.view_date, date_pattern='yyyy-mm-dd',
                            font=("goudy old style", 12), bg="#e1f0f7", width=12)
        view_cal.pack(side=LEFT, padx=10)
        view_cal.bind("<<DateEntrySelected>>", lambda e: self.update_attendance_list(view_window))
        Label(title_frame, text=f"{self.var_course.get()}", font=("goudy old style", 16, "bold"), bg="#4A90E2", fg="white").pack(side=LEFT, padx=10)

        attendance_frame = Frame(view_window, bd=0, relief=FLAT, bg="#FFFFFF")
        attendance_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        header_frame = Frame(attendance_frame, bg="#2C3E50", bd=0, relief=FLAT)
        header_frame.pack(fill=X)
        Label(header_frame, text="Roll", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=10).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Name", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=15).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Date", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=12).pack(side=LEFT, padx=10, pady=5)
        Label(header_frame, text="Status", font=("goudy old style", 12, "bold"), bg="#2C3E50", fg="white", width=12).pack(side=LEFT, padx=10, pady=5)

        canvas = Canvas(attendance_frame, bg="#FFFFFF")
        scrollbar = Scrollbar(attendance_frame, orient=VERTICAL, command=canvas.yview)
        self.attendance_inner_frame = Frame(canvas, bg="#FFFFFF")
        
        

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.create_window((0, 0), window=self.attendance_inner_frame, anchor="nw")
        self.attendance_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.update_attendance_list(view_window)

    def update_attendance_list(self, view_window):
        for widget in self.attendance_inner_frame.winfo_children():
            widget.destroy()

        try:
            datetime.strptime(self.view_date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.", parent=view_window)
            return

        con = sqlite3.connect(database="sms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT cid FROM course WHERE name=?", (self.var_course.get(),))
            course_id = cur.fetchone()
            if not course_id:
                messagebox.showerror("Error", "Invalid course", parent=view_window)
                view_window.destroy()
                return
            course_id = course_id[0]

            cur.execute("""
                SELECT a.roll, s.name, a.date, a.status 
                FROM attendance a 
                JOIN student s ON a.roll = s.roll 
                WHERE a.course = ? AND a.date = ?
            """, (course_id, self.view_date.get()))
            rows = cur.fetchall()

            if len(rows) > 0:
                for idx, (roll, name, date, status) in enumerate(rows):
                    frame = Frame(self.attendance_inner_frame, bg="#FFFFFF" if idx % 2 == 0 else "#F5F5F5", bd=0, relief=FLAT)
                    frame.pack(fill=X, pady=10)
                    Label(frame, text=str(roll), font=("goudy old style", 12), bg=frame.cget("bg"), width=10).pack(side=LEFT, padx=10, pady=5)
                    Label(frame, text=name, font=("goudy old style", 12), bg=frame.cget("bg"), width=15).pack(side=LEFT, padx=10, pady=5)
                    Label(frame, text=date, font=("goudy old style", 12), bg=frame.cget("bg"), width=12).pack(side=LEFT, padx=10, pady=5)
                    status_color = "#28A745" if status == "P" else "#DC3545"
                    Label(frame, text="Present" if status == "P" else "Absent", font=("goudy old style", 12, "bold"), bg=frame.cget("bg"), fg=status_color, width=12).pack(side=LEFT, padx=10, pady=5)
            else:
                Label(self.attendance_inner_frame, text="No attendance records found for this date.", font=("goudy old style", 12), bg="#FFFFFF").pack(pady=10)

        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Error fetching attendance: {str(ex)}", parent=view_window)
            view_window.destroy()
        finally:
            con.close()


    def generate_attendance_report(self):   
        if self.var_course.get() == "Select":
            messagebox.showerror("Error", "Please select a course", parent=self.root)
            return

        report_window = Toplevel(self.root)
        report_window.title("Generate Attendance Report")
        report_window.geometry("400x200")
        self.center_window(report_window, 400, 200)
        report_window.config(bg="#F5F7FA")

        Label(report_window, text="Select Month and Year", font=("goudy old style", 14, "bold"), 
            bg="#F5F7FA").pack(pady=10)

        month_frame = Frame(report_window, bg="#F5F7FA")
        month_frame.pack(pady=5)
        
        Label(month_frame, text="Month:", font=("goudy old style", 12), bg="#F5F7FA").pack(side=LEFT, padx=5)
        month_var = StringVar(value=datetime.now().strftime("%m"))
        month_combo = ttk.Combobox(month_frame, textvariable=month_var, 
                                values=[f"{i:02d}" for i in range(1, 13)],
                                state='readonly', width=5)
        month_combo.pack(side=LEFT, padx=5)

        Label(month_frame, text="Year:", font=("goudy old style", 12), bg="#F5F7FA").pack(side=LEFT, padx=5)
        year_var = StringVar(value=datetime.now().strftime("%Y"))
        year_combo = ttk.Combobox(month_frame, textvariable=year_var,
                                values=[str(i) for i in range(2020, 2026)],
                                state='readonly', width=6)
        year_combo.pack(side=LEFT, padx=5)

        def generate_csv():
            month = month_var.get()
            year = year_var.get()
            
            try:
                selected_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
                _, days_in_month = monthrange(int(year), int(month))
            except ValueError:
                messagebox.showerror("Error", "Invalid month or year", parent=report_window)
                return

            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            
            try:
                cur.execute("SELECT cid FROM course WHERE name=?", (self.var_course.get(),))
                course_id = cur.fetchone()
                if not course_id:
                    messagebox.showerror("Error", "Invalid course", parent=report_window)
                    return
                course_id = course_id[0]

                cur.execute("SELECT roll, name FROM student WHERE course=?", (self.var_course.get(),))
                students = cur.fetchall()
                
                if not students:
                    messagebox.showerror("Error", "No students found for this course", parent=report_window)
                    return

                attendance_data = {}
                for roll, name in students:
                    cur.execute("""
                        SELECT date, status 
                        FROM attendance 
                        WHERE roll=? AND course=? AND date LIKE ? 
                        ORDER BY date
                    """, (roll, course_id, f"{year}-{month}%"))
                    attendance_data[roll] = {"name": name, "dates": dict(cur.fetchall())}

                filename = f"attendance_{self.var_course.get().replace(' ', '_')}_{year}_{month}.csv"
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['Roll', 'Name'] + [f"{year}-{month}-{str(i).zfill(2)}" 
                                                for i in range(1, days_in_month + 1)]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                    for roll in attendance_data:
                        row = {'Roll': roll, 'Name': attendance_data[roll]['name']}
                        for day in range(1, days_in_month + 1):
                            date = f"{year}-{month}-{str(day).zfill(2)}"
                            status = attendance_data[roll]['dates'].get(date, '-')
                            row[date] = status
                        writer.writerow(row)

                messagebox.showinfo("Success", f"Attendance report saved as {filename}", 
                                parent=report_window)
                report_window.destroy()

            except sqlite3.Error as ex:
                messagebox.showerror("Error", f"Error generating report: {str(ex)}", 
                                parent=report_window)
            finally:
                con.close()

        submit_btn = Button(report_window, text="Submit", font=("goudy old style", 12),
                        bg="#28A745", fg="white", command=generate_csv)
        submit_btn.pack(pady=20)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#218838"))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#28A745"))



    def clear(self):
        self.var_course.set("Select")
        self.student_data.clear()
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        Label(self.inner_frame, text="Please select a course.", font=("goudy old style", 12), bg="#FFFFFF").pack(pady=10)
        self.lbl_present.config(text="Present: 0")
        self.lbl_absent.config(text="Absent: 0")

    def center_window(self, window=None, width=1200, height=650):
        if window is None:
            window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x_position}+{y_position}")

if __name__ == "__main__":
    root = Tk()
    obj = AttendanceClass(root)
    root.mainloop()