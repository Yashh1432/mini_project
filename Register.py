import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
# from dashbord2_demo import SMS
# from Login import Login

class Register:
    def __init__(self, root, login_callback):
        self.root = root
        self.root.title("Register - Student Management System")
        self.root.geometry("1520x785+0+0")
        self.root.config(bg="white")
        self.login_callback = login_callback    
        
        
        # Background Image
        try:
            bg_image = Image.open("img/bg_register.jpg").convert("RGBA")
        except FileNotFoundError:
            bg_image = Image.new("RGBA", (1520, 785), (255, 255, 255, 255))  # Fallback white background
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_image = self.reduce_opacity(bg_image, 100)
        self.bg = ImageTk.PhotoImage(bg_image)
        Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # Left Image
        try:
            left_image = Image.open("img/register.png").resize((400, 500), Image.Resampling.LANCZOS)
            
        except FileNotFoundError:
            left_image = Image.new("RGB", (400, 500), "gray")  # Fallback gray image
        self.left = ImageTk.PhotoImage(left_image)
        Label(self.root, image=self.left).place(x=220, y=130, width=400, height=500)

        # Register Frame
        frame1 = Frame(self.root, bg="white", bd=5, relief=RIDGE)
        frame1.place(x=650, y=130, width=600, height=500)

        # Title
        Label(frame1, text="REGISTER HERE", font=("goudy old style", 20, "bold"),
              bg="white", fg="#17A2B8").place(x=200, y=30)

        # First Name
        Label(frame1, text="First Name:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=50, y=80)
        self.txt_fname = Entry(frame1, font=("goudy old style", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=110, width=220)

        # Last Name
        Label(frame1, text="Last Name:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=300, y=80)
        self.txt_lname = Entry(frame1, font=("goudy old style", 15), bg="lightgray")
        self.txt_lname.place(x=300, y=110, width=220)

        # Contact
        Label(frame1, text="Contact No:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=50, y=150)
        self.txt_contact = Entry(frame1, font=("goudy old style", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=180, width=220)

        # Email
        Label(frame1, text="Email:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=300, y=150)
        self.txt_email = Entry(frame1, font=("goudy old style", 15), bg="lightgray")
        self.txt_email.place(x=300, y=180, width=220)

        # Security Question
        Label(frame1, text="Security Question:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=50, y=220)
        self.cmd_quest = ttk.Combobox(frame1, font=("goudy old style", 13), state='readonly', justify=CENTER)
        self.cmd_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
        self.cmd_quest.place(x=50, y=250, width=220)
        self.cmd_quest.current(0)

        # Answer
        Label(frame1, text="Answer:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=300, y=220)
        self.txt_answer = Entry(frame1, font=("goudy old style", 15), bg="lightgray")
        self.txt_answer.place(x=300, y=250, width=220)

        # Password
        Label(frame1, text="Password:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=50, y=290)
        self.txt_password = Entry(frame1, font=("goudy old style", 15), bg="lightgray", show="*")
        self.txt_password.place(x=50, y=320, width=220)

        # Confirm Password
        Label(frame1, text="Confirm Password:", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=300, y=290)
        self.txt_cpassword = Entry(frame1, font=("goudy old style", 15), bg="lightgray", show="*")
        self.txt_cpassword.place(x=300, y=320, width=220)

        # Terms & Conditions
        self.var_chk = IntVar()
        Checkbutton(frame1, text="I Agree to the Terms & Conditions", variable=self.var_chk, onvalue=1, offvalue=0,
                    bg="white", font=("goudy old style", 12, 'bold')).place(x=50, y=360)

        # Register Button
        Button(frame1, text="Register!!", bd=0, font=("goudy old style", 14, "bold"), cursor="hand2", bg="#17A2B8", fg="white",
               activebackground="#138496", activeforeground="white", command=self.register_data).place(x=200, y=450, width=220, height=30)

      # Sign In Button (Redirects to Login)
        Button(frame1, text="Already have an account? Sign In", font=("goudy old style", 14), bd=0, cursor="hand2",
               bg="white", fg="#2F8F9D", command=self.redirect_to_login).place(x=150, y=400, width=300, height=30)
        
    def clear(self):
        """Clears all input fields."""
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmd_quest.current(0)

    def validate_email(self, email):
        """Basic email validation."""
        return "@" in email and "." in email.split("@")[1]

    def validate_contact(self, contact):
        """Validate contact number."""
        return contact.isdigit() and len(contact) == 10

    def validate_password(self, password):
        """Ensure password is at least 6 characters."""
        return len(password) >= 6

    def register_data(self):
        """Handles the user registration process with redirection to login."""
        fname = self.txt_fname.get().strip()
        lname = self.txt_lname.get().strip()
        contact = self.txt_contact.get().strip()
        email = self.txt_email.get().strip()
        question = self.cmd_quest.get()
        answer = self.txt_answer.get().strip()
        password = self.txt_password.get().strip()
        cpassword = self.txt_cpassword.get().strip()

        if not all([fname, lname, contact, email, question != "Select", answer, password, cpassword]):
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        elif not self.validate_email(email):
            messagebox.showerror("Error", "Invalid Email Format", parent=self.root)
        elif not self.validate_contact(contact):
            messagebox.showerror("Error", "Contact Number Must Be 10 Digits", parent=self.root)
        elif not self.validate_password(password):
            messagebox.showerror("Error", "Password Must Be At Least 6 Characters", parent=self.root)
        elif password != cpassword:
            messagebox.showerror("Error", "Password and Confirm Password Must Match", parent=self.root)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please Agree to the Terms & Conditions", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="sms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM register WHERE email=?", (email,))
                row = cur.fetchone()

                if row:
                    messagebox.showerror("Error", "Email Already Exists, Please Login", parent=self.root)
                else:
                    cur.execute("""
                        INSERT INTO register (f_name, l_name, contact, email, question, answer, password)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (fname, lname, contact, email, question, answer, password))
                    con.commit()
                    messagebox.showinfo("Success", "Registration Successful! Redirecting to Login...", parent=self.root)
                    self.clear()
                    self.login_callback()  # Redirect to login after successful registration
                con.close()
            except sqlite3.Error as err:
                messagebox.showerror("Error", f"Database Error: {str(err)}", parent=self.root)

    def reduce_opacity(self, img, opacity):
        """Reduces image opacity."""
        r, g, b, a = img.split()
        a = a.point(lambda i: i * (opacity / 255))
        return Image.merge("RGBA", (r, g, b, a))
    
    def redirect_to_login(self):
        """Redirects to the login page."""
        print("Redirecting to login page...")  # Debug
        self.login_callback()

if __name__ == "__main__":
    root = Tk()
    obj = Register(root, lambda: print("Login would open here"))    
    root.mainloop()