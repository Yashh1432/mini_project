import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Login import Login
from Register import Register
from course import CourseClass
from studentdemo import studentClass
from result import resultClass
from report import ReportClass
from attendance import AttendanceClass

class SMS:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Student Management System !!")
        self.root.config(bg="white")

    #     # Start with Register window
        self.show_login()

    def show_register(self):
        print("Opening Register Page")  # Debug
        for widget in self.root.winfo_children():   
            widget.destroy()
        Register(self.root, self.show_login)

    def show_login(self):
        print("Opening Login Page")  # Debug
        for widget in self.root.winfo_children():
            widget.destroy()
        # Pass the dashboard callback as a lambda to ensure proper binding
        Login(self.root, lambda: self.show_dashboard())

    def show_dashboard(self):
        print("Opening Dashboard")  # Debug
        for widget in self.root.winfo_children():
            widget.destroy()
            

        # Sidebar Frame
        sidebar_width = int(self.root.winfo_screenwidth() * 0.14)
        sidebar_height = self.root.winfo_screenheight()
        self.sidebar_frame = Frame(self.root, bg="#2F8F9D", width=sidebar_width, height=sidebar_height)
        self.sidebar_frame.place(x=0, y=0, width=sidebar_width, height=sidebar_height)

        # Logo inside Sidebar
        logo_size = int(sidebar_width * 0.8)
        try:
            logo = Image.open("img/logo.png")
        except FileNotFoundError:
            logo = Image.new("RGB", (logo_size, logo_size), "#2F8F9D")
        logo = logo.resize((logo_size, logo_size))
        self.logo_dash = ImageTk.PhotoImage(logo)
        logo_label = Label(self.sidebar_frame, image=self.logo_dash, bg="#2F8F9D")
        logo_label.pack(pady=20)

        # Sidebar Buttons
        button_style = {"font": ("goudy old style", 15, "bold"), "bg": "#82DBD8", "cursor": "hand2", "fg": "black", "width": 15, "height": 2}
        btn_course = Button(self.sidebar_frame, text="Course", command=self.add_course, **button_style)
        btn_course.pack(pady=10)
        btn_student = Button(self.sidebar_frame, text="Student", command=self.add_student, **button_style)
        btn_student.pack(pady=10)
        btn_result = Button(self.sidebar_frame, text="Result", command=self.add_result, **button_style)
        btn_result.pack(pady=10)
        btn_viewResult = Button(self.sidebar_frame, text="View Result", command=self.view_result, **button_style)
        btn_viewResult.pack(pady=10)
        btn_attendance = Button(self.sidebar_frame, text="Attendance", command=self.add_attandance, **button_style)
        btn_attendance.pack(pady=10)
        btn_logout = Button(self.sidebar_frame, text="Logout", command=self.logout, **button_style)
        btn_logout.pack(pady=10)

        # Main Content Area
        main_area = Frame(self.root, bg="#F5F5F5")
        main_area.place(x=sidebar_width + 12, y=10, width=self.root.winfo_screenwidth() - sidebar_width - 20, height=self.root.winfo_screenheight() - 45)

        welcome_label = Label(main_area, text="Welcome to the Student Management System", font=("goudy old style", 30, "bold"), bg="#F5F5F5", fg="#3BACB6")
        welcome_label.pack(pady=10)

        # Background Image
        try:
            bg_img = Image.open("img/7.jpg")
        except FileNotFoundError:
            bg_img = Image.new("RGB", (self.root.winfo_screenwidth() - sidebar_width - 20, int(self.root.winfo_screenheight() * 0.6)), "#F5F5F5")
        bg_img = bg_img.resize((self.root.winfo_screenwidth() - sidebar_width - 20, int(self.root.winfo_screenheight() * 0.6)))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        lbl_bg = Label(main_area, image=self.bg_img, bg="#F5F5F5")
        lbl_bg.pack(side=TOP, anchor="center", pady=10)

        # Info Boxes (Bottom)
        info_frame = Frame(main_area, bg="#F5F5F5")
        info_frame.pack(side=TOP, fill=X, pady=10)
        box_style = {"font": ("montserrat", 18), "bd": 8, "relief": RIDGE, "width": 25, "height": 3}

        self.lbl_course = Label(info_frame, text="Total Courses\n[ ]", bg="#3BACB6", fg="white", **box_style)
        self.lbl_course.grid(row=0, column=0, padx=15, pady=5)
        self.lbl_student = Label(info_frame, text="Total Students\n[ ]", bg="#B3E8E5", fg="black", **box_style)
        self.lbl_student.grid(row=0, column=1, padx=15, pady=5)
        self.lbl_result = Label(info_frame, text="Total Results\n[ ]", bg="#3BACB6", fg="white", **box_style)
        self.lbl_result.grid(row=0, column=2, padx=15, pady=5)

        self.update_counts()

        # Footer
        footer = Label(self.root, text="Student Management System | GUJJU infotech | Contact Us: 7874273210",
                       font=("goudy old style", 12), bg="#2F8F9D", fg="black")
        footer.pack(side=BOTTOM, fill=X)
        self.root.update()

    def update_counts(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM course")
            total_courses = cur.fetchone()[0]
            self.lbl_course.config(text=f"Total Courses\n[ {total_courses} ]")
            cur.execute("SELECT COUNT(*) FROM student")
            total_students = cur.fetchone()[0]
            self.lbl_student.config(text=f"Total Students\n[ {total_students} ]")
            cur.execute("SELECT COUNT(*) FROM result")
            total_results = cur.fetchone()[0]
            self.lbl_result.config(text=f"Total Results\n[ {total_results} ]")
            con.close()
        except sqlite3.Error as ex:
            print(f"Error fetching counts: {str(ex)}")

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)

    def view_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ReportClass(self.new_win)

    def add_attandance(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = AttendanceClass(self.new_win)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root):
            self.show_login()  # Redirect to login without destroying the root

if __name__ == "__main__":
    root = Tk()
    app = SMS(root)
    root.mainloop()