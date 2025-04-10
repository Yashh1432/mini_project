from tkinter import *
from PIL import Image, ImageTk
from course import CourseClass
# from student import studentClass
# from result import resultClass
# from report import ReportClass

class SMS:
    def __init__(self, root):
        self.root = root
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set the window to full screen or a calculated size
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Student Management System !!")
        self.root.config(bg="white")

        logo = Image.open("img/logo.png")
        logo_size = int(screen_height * 0.1)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        self.logo_dash = ImageTk.PhotoImage(logo)

        # Title Label
        title_height = int(screen_height * 0.07)
        title = Label(
            self.root,
            text="Student Management System ",
            padx=20,
            compound=LEFT,
            image=self.logo_dash,
            font=("goudy old style", 25, "bold"),
            bg="#2F8F9D",
            fg="white"
        )
        title.place(x=0, y=0, relwidth=1, height=title_height)
        
        # Menu Frame 
        menu_frame_height = int(screen_height * 0.1)
        M_Frames = LabelFrame(
            self.root,
            text="Menus",
            font=("Times New Roman", 15),
            bg="white",
            bd=2,
            relief=RIDGE
        )
        M_Frames.place(x=10, y=title_height, width=screen_width-20, height=menu_frame_height)
         
        # Course Button inside Menu Frame
        btn_course = Button(
            M_Frames,
            text="Course",
            font=("goudy old style", 15, "bold"),
            bg="#82DBD8",
            cursor="hand2",
            command=self.add_course,
            fg="black"
        )
        btn_course.place(x=20, y=5, width=220, height=40)
        
        btn_student = Button(
            M_Frames,
            text="Student",
            font=("goudy old style", 15, "bold"),
            bg="#82DBD8",
            cursor="hand2",
            fg="black"
        )
        btn_student.place(x=260, y=5, width=220, height=40)
        
        btn_Result = Button(
            M_Frames,
            text="Result",
            font=("goudy old style", 15, "bold"),
            bg="#82DBD8",
            cursor="hand2",
            fg="black"
        )
        btn_Result.place(x=510, y=5, width=220, height=40)
        
        btn_viewResult = Button(
            M_Frames,
            text="View Result",
            font=("goudy old style", 15, "bold"),
            bg="#82DBD8",
            cursor="hand2",
            fg="black"
        )
        btn_viewResult.place(x=770, y=5, width=220, height=40)
        
        btn_attendance = Button(
            M_Frames,
            text="Attendance",
            font=("goudy old style", 15, "bold"),
            bg="#82DBD8",
            cursor="hand2",
            fg="black"
        )
        btn_attendance.place(x=1020, y=5, width=220, height=40)

        btn_logout = Button(
            M_Frames,
            text="Logout",
            font=("goudy old style", 15, "bold"),
            bg="#82DBD8",
            cursor="hand2",
            fg="black"
        )
        btn_logout.place(x=1270, y=5, width=220, height=40)
        
        main_area = Frame(self.root, bg="#F5F5F5")
        main_area.place(x=20, y=title_height + menu_frame_height + 20,
                        width=screen_width - 40, height=screen_height - title_height - menu_frame_height - 80)
        
        
        welcome_label = Label(main_area,
                              text="Welcome to the Student Management System",
                              font=("goudy old style", 22),
                              bg="#F5F5F5",
                              fg="#333333")
        welcome_label.pack(pady=20)
        
        
        # # content window
        # self.bg_img = Image.open("img/5251.jpg")
        # self.bg_img = self.bg_img.resize((1000, 400), Image.Resampling.LANCZOS)
        # self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # self.lbl_bg = Label(self.root, image=self.bg_img)
        # self.lbl_bg.place(x=1, y=250, width=1510, height=500)
        
        
        # # Update
        # self.lbl_course=Label(self.root,text="Total Courses\n[ 0 ]",font=("montserrat",20),bd=10,relief=RIDGE,bg="#232323",fg="white")
        # self.lbl_course.place(x=400,y=620,width=300,height=100)

        # self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("montserrat",20),bd=10,relief=RIDGE,bg="#6ca0dc",fg="black")
        # self.lbl_student.place(x=805,y=620,width=300,height=100)

        # self.lbl_result=Label(self.root,text="Total Results\n[ 0 ]",font=("montserrat",20),bd=10,relief=RIDGE,bg="#232323",fg="white")
        # self.lbl_result.place(x=1210,y=620,width=300,height=100)

        
                # Set a medium-size background image within the main area
        self.bg_img = Image.open("img/bdimg.png")
        bg_width = int((screen_width - 70) * 0.8)
        bg_height = int((screen_height - title_height - menu_frame_height - 180) * 0.9)
        self.bg_img = self.bg_img.resize((bg_width, bg_height), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg = Label(main_area, image=self.bg_img)
        # Center the background image within main_area
        self.lbl_bg.place(x=(screen_width - 40 - bg_width)//2, y=80, width=bg_width, height=bg_height)
        
        # -------------------- Info Boxes (aligned at the bottom) --------------------
        box_width = 280
        box_height = 90
        gap = 20
        total_width = (box_width * 3) + (gap * 2)
        start_x = (screen_width - 40 - total_width) // 2
        info_y = title_height + menu_frame_height + 20 + (screen_height - title_height - menu_frame_height - 180) - box_height - 20

        self.lbl_course = Label(
            self.root,
            text="Total Courses\n[ 0 ]",
            font=("montserrat", 18),
            bd=8,
            relief=RIDGE,
            bg="#3BACB6",
            fg="white"
        )
        self.lbl_course.place(x=start_x, y=info_y, width=box_width, height=box_height)

        self.lbl_student = Label(
            self.root,
            text="Total Students\n[ 0 ]",
            font=("montserrat", 18),
            bd=8,
            relief=RIDGE,
            bg="#B3E8E5",
            fg="black"
        )
        self.lbl_student.place(x=start_x + box_width + gap, y=info_y, width=box_width, height=box_height)

        self.lbl_result = Label(
            self.root,
            text="Total Results\n[ 0 ]",
            font=("montserrat", 18),
            bd=8,
            relief=RIDGE,
            bg="#3BACB6",
            fg="white"
        )
        self.lbl_result.place(x=start_x + (box_width + gap)*2, y=info_y, width=box_width, height=box_height)
        
        # Footer inside __init__
        footer = Label(
            self.root,
            text="Student management System \\ contact us for any Technical Issue : 7874273210",
            font=("goudy old style", 15, "bold"),
            bg="#B3E8E5",
            fg="black"
        )
        footer.pack(side=BOTTOM, fill=X)
        
        
        # # Footer (Ensuring it's always visible)
        # footer = Label(self.root, text="Student Management System | Contact Us: 7874273210", font=("goudy old style", 14, "bold"), bg="#B3E8E5", fg="black")
        # footer.place(x=0, y=screen_height - 40, width=screen_width, height=40)  # Fixed position at the bottom

        
    def add_course(self):
        self.new_win=Toplevel(self.root)    
        self.new_obj=CourseClass(self.new_win)


if __name__ == "__main__":
    root = Tk()
    app = SMS(root)
    root.mainloop()
