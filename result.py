
# import mysql.connector
import sqlite3
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter import ttk, messagebox


class resultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.config(bg="white")
        self.root.update_idletasks()  # Ensure Tkinter initializes before setting geometry
        self.center_window()
        self.root.focus_force()
        
        
    #     # Start with Register window
        # Title
        title = Label(self.root, text="Add Student Results !!", padx=10, compound=LEFT, 
                      font=("goudy old style", 25, "bold"), bg="#B3E8E5", fg="black")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Widgets
        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()

        lbl_select = Label(self.root, text="Select Student:", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=100)
        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=160)
        lbl_course = Label(self.root, text="Course:", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=220)
        lbl_marks = Label(self.root, text="Marks Obtained:", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=280)
        lbl_full_marks = Label(self.root, text="Full Marks:", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=340)

        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=("goudy old style", 19, 'bold'), state='readonly', justify=CENTER)
        self.txt_student.place(x=320, y=105, width=200)
        self.txt_student.set("Select")

        btn_search = Button(self.root, text="Search", font=("goudy old style", 20, 'bold'), bg="#17A2B8", fg="black", cursor="hand2", command=self.search).place(x=550, y=105, width=120, height=40)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 20, 'bold'), bg="#e1f0f7", state="readonly").place(x=320, y=165, width=350)
        txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 20, 'bold'), bg="#e1f0f7", state="readonly").place(x=320, y=225, width=350)
        txt_marks = Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 20, 'bold'), bg="#e1f0f7").place(x=320, y=285, width=350)
        txt_full_marks = Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 20, 'bold'), bg="#e1f0f7").place(x=320, y=345, width=350)

        # Button
        btn_add = Button(self.root, text="Submit", font=("goudy old style", 20), bg="green", fg="white", activebackground="green", cursor="hand2", command=self.add).place(x=320, y=465, width=150, height=40)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 20), bg="red", fg="white", activebackground="red", cursor="hand2", command=self.clear).place(x=520, y=465, width=150, height=40)

        # Content Window
        self.target_width = 720  # Width of the image area
        self.target_height = 500  # Height of the image area
        
        # Load and resize image while maintaining aspect ratio
        original_img = Image.open("D:/sem_2/MINI_PROJECT/img/3.jpg")
        
        # Calculate aspect ratio and new dimensions
        img_width, img_height = original_img.size
        aspect_ratio = img_width / img_height
        
        # Determine new size while maintaining aspect ratio
        if (self.target_width / self.target_height) > aspect_ratio:
            # Fit to height
            new_height = self.target_height
            new_width = int(new_height * aspect_ratio)
        else:
            # Fit to width
            new_width = self.target_width
            new_height = int(new_width / aspect_ratio)
        
        # Resize image with high-quality downscaling
        resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.bg_img = ImageTk.PhotoImage(resized_img)

        self.lbl_bg = Label(self.root, image=self.bg_img)
        self.lbl_bg.place(x=700, y=105, width=490, height=500)

        # Footer
        footer = Label(self.root, text="Student Management System | GUJJU infotech | Contact Us: 7874273210",
                       font=("goudy old style", 12),  bg="#2F8F9D", fg="black")
        footer.pack(side=BOTTOM, fill=X)
        
        
        
        
    def search(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row is not None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def add(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Please first search student record", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE roll=? AND course=?", (self.var_roll.get(), self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Result already present", parent=self.root)
                else:
                    per = (int(self.var_marks.get()) * 100) / int(self.var_full_marks.get())
                    cur.execute("INSERT INTO result (roll, name, course, marks_ob, full_marks, per) VALUES (?, ?, ?, ?, ?, ?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get(),
                        str(per)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")

    def fetch_roll(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
        try:
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def center_window(self, width=1250, height=650):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")

if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()