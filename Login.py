import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from Register import Register


class Login:
    def __init__(self, root, dashboard_callback):
        self.root = root
        self.root.title("Login - Student Management System")
        self.root.geometry("1820x785+0+0")
        self.root.config(bg="#021e2f")
        self.dashboard_callback = dashboard_callback

        # Background Image
        try:
            bg_image = Image.open("img/bg_register.jpg").convert("RGBA")
        except FileNotFoundError:
            bg_image = Image.new("RGBA", (1520, 785), (255, 255, 255, 255))  # Fallback white background
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_image = self.reduce_opacity(bg_image, 100)
        self.bg = ImageTk.PhotoImage(bg_image)
        Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)


        # Login Frame (Matching SMS design)
        login_frame = Frame(self.root, bg="white", bd=4, relief=RIDGE)
        login_frame.place(x=370, y=130, width=850, height=550)

        # Title
        Label(login_frame, text="Login to Your Account", font=("goudy old style", 25, "bold","underline"),
              bg="white", fg="#2F8F9D").place(x=250, y=30)

        # Email
        Label(login_frame, text="Email Address:", font=("goudy old style", 15, "bold"),
              bg="white", fg="#021e2f").place(x=50, y=150)
        self.txt_email = Entry(login_frame, font=("goudy old style", 15), bg="#F5F5F5", bd=2, relief=GROOVE)
        self.txt_email.place(x=50, y=190, width=350)

        # Password
        Label(login_frame, text="Password:", font=("goudy old style", 15, "bold"),
              bg="white", fg="#021e2f").place(x=50, y=250)
        self.txt_password = Entry(login_frame, font=("goudy old style", 15), bg="#F5F5F5", show="*", bd=2, relief=GROOVE)
        self.txt_password.place(x=50, y=290, width=350)

        # Register Link
        Button(login_frame, text="New User? Register Here", font=("goudy old style", 15), bg="white", bd=0,
               fg="#2F8F9D", cursor="hand2", command=self.register_link).place(x=50, y=350)

        Button(login_frame, text="Forget Password?", font=("goudy old style", 15), bg="white", bd=0,
               fg="red", cursor="hand2", command=self.forget_password).place(x=280, y=350)
        
        # Login Button (Styled like SMS buttons)
        Button(login_frame, text="Sign In", font=("goudy old style", 20, "bold"), bg="#2F8F9D", fg="white",
               bd=0, cursor="hand2", activebackground="#82DBD8", activeforeground="black",
               command=self.login).place(x=50, y=400, width=350, height=50)

        # Right Image
        try:
            right_image = Image.open("img/login.jpg")
        except FileNotFoundError:
            right_image = Image.new("RGB", (370, 430), "#F5F5F5")  # Fallback
        right_image = right_image.resize((370, 430), Image.Resampling.LANCZOS)
        self.right_img = ImageTk.PhotoImage(right_image)
        Label(login_frame, image=self.right_img, bg="white").place(x=450, y=80, width=370, height=430)
        
        
    
    def reduce_opacity(self, img, opacity):
        """Reduces image opacity."""
        r, g, b, a = img.split()
        a = a.point(lambda i: i * (opacity / 255))
        return Image.merge("RGBA", (r, g, b, a))
    

    def register_link(self):
            for widget in self.root.winfo_children():
                widget.destroy()
            Register(self.root, self.show_login)

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Login(self.root, self.dashboard_callback)

    def validate_email(self, email):
        """Basic email validation"""
        return "@" in email and "." in email.split("@")[1]


    def forget_password(self):
        if self.txt_email.get() == "":
            messagebox.showerror("Error", "Please enter the email address to reset your password", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="sms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM register WHERE email=?", (self.txt_email.get(),))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error", "Please enter a valid email address to reset your password", parent=self.root)
                else:
                    con.close()
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("450x480+340+150")
                    self.root2.config(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    # Title
                    t = Label(self.root2, text=".......Forget Password.......", font=("goudy old style", 23, "bold", "underline"), bg="white", fg="red")
                    t.place(x=0, y=10, relwidth=1)

                    # Security Question
                    question = Label(self.root2, text="Security Question:", font=("goudy old style", 15, "bold"), bg="white", fg="black")
                    question.place(x=40, y=80)
                    self.cmd_quest = ttk.Combobox(self.root2, font=("goudy old style", 13), state='readonly', justify=CENTER)
                    self.cmd_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
                    self.cmd_quest.place(x=40, y=130, width=370)
                    self.cmd_quest.current(0)

                    # Answer
                    answer = Label(self.root2, text="Answer:", font=("goudy old style", 15, "bold"), bg="white", fg="black")
                    answer.place(x=40, y=190)
                    self.txt_answer = Entry(self.root2, font=("goudy old style", 15), bg="lightgray")
                    self.txt_answer.place(x=40, y=230, width=370)

                    # New Password
                    new_password = Label(self.root2, text="New Password:", font=("goudy old style", 15, "bold"), bg="white", fg="black")
                    new_password.place(x=40, y=290)
                    self.txt_new_pass = Entry(self.root2, font=("goudy old style", 15), bg="lightgray")
                    self.txt_new_pass.place(x=40, y=330, width=370)

                    # Reset Password Button
                    btn_change_password = Button(self.root2, text="Reset Password", bg="green", fg="white", cursor="hand2",
                                                font=("goudy old style", 15, "bold"), command=self.reset_password)
                    btn_change_password.place(x=100, y=400, width=250)

            except sqlite3.Error as es:
                messagebox.showerror("Error", f"Database Error: {str(es)}", parent=self.root)

    def reset_password(self):
        if self.cmd_quest.get() == "Select":
            messagebox.showerror("Error", "Please select a security question", parent=self.root2)
        elif self.txt_answer.get() == "":
            messagebox.showerror("Error", "Please enter the answer", parent=self.root2)
        elif self.txt_new_pass.get() == "":
            messagebox.showerror("Error", "Please enter new password", parent=self.root2)
        else:
            try:
                con = sqlite3.connect(database="sms.db")
                cur = con.cursor()

                # Verify security question and answer
                cur.execute("SELECT * FROM register WHERE email=? AND question=? AND answer=?",
                            (self.txt_email.get(), self.cmd_quest.get(), self.txt_answer.get()))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error", "Security answer is incorrect", parent=self.root2)
                else:
                    # Update password
                    cur.execute("UPDATE register SET password=? WHERE email=?",
                                (self.txt_new_pass.get(), self.txt_email.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Password has been reset successfully", parent=self.root2)
                    self.root2.destroy()

            except sqlite3.Error as es:
                messagebox.showerror("Error", f"Database Error: {str(es)}", parent=self.root2)
            finally:
                con.close()
    def login(self):
        email = self.txt_email.get().strip()
        password = self.txt_password.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and Password are Required", parent=self.root)
        elif not self.validate_email(email):
            messagebox.showerror("Error", "Invalid Email Format", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="sms.db")
                cur = con.cursor()
                cur.execute("SELECT f_name, l_name FROM register WHERE email=? AND password=?",
                            (email, password))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome, {row[0]} {row[1]}!", parent=self.root)
                    print("Login successful, redirecting to dashboard...")  # Debug
                    self.dashboard_callback()  # Redirect to dashboard
                    # self.open_dashboard()  # Call function to open dashboard

                con.close()
            except sqlite3.Error as err:
                messagebox.showerror("Error", f"Database Error: {str(err)}", parent=self.root) 
                

    # def open_dashboard(self):
    #     self.root.destroy()  # Close login window
    #     from dashbord2_demo import SMS  # Import the Dashboard class
    #     root = Tk()  # Create a new root
    #     obj=SMS(root)  # Open the dashboard
    #     root.mainloop()  # Start Tkinter main loop
        
if __name__ == "__main__":
    root = Tk()
    obj = Login(root, lambda: print("Dashboard would open here"))
    root.mainloop()