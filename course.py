from PIL import Image, ImageTk,ImageSequence
from tkinter import ttk, messagebox
from tkinter import *
import sqlite3
import re

# import mysql.connector 


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x480+80+170")
        self.root.title("Student Management System !!")
        self.root.config(bg="white")
        self.root.focus_force()
        
        
        
        # self.con = mysql.connector.connect(host="localhost", user="root", password="yash1432", database="sms")
        # self.cur = self.con.cursor()
        

        
        
        # Title=========================
        title = Label(self.root, text="Manage Course Details !!", padx=10, compound=LEFT, 
                      font=("goudy old style", 25, "bold"), bg="#B3E8E5", fg="black")
        title.place(x=0, y=0, relwidth=1, height=50)
        
        # Variables======================
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        
        # Labels=========================
        lbl_course = Label(self.root, text="Course Name:", font=("goudy old style", 15, 'bold'), bg="white")
        lbl_course.place(x=10, y=70)
        
        lbl_duration = Label(self.root, text="Duration:", font=("goudy old style", 15, 'bold'), bg="white")
        lbl_duration.place(x=10, y=130)
        
        lbl_charges = Label(self.root, text="Charges:", font=("goudy old style", 15, 'bold'), bg="white")
        lbl_charges.place(x=10, y=190)
        
        lbl_description = Label(self.root, text="Description:", font=("goudy old style", 15, 'bold'), bg="white")
        lbl_description.place(x=10, y=250)
        
        # Entry Fields=====================
        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, 'bold'), bg="#e1f0f7")
        self.txt_courseName.place(x=150, y=70, width=200)
        
        self.txt_duration = Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15, 'bold'), bg="#e1f0f7")
        self.txt_duration.place(x=150, y=130, width=200)
        
        self.txt_charges = Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15, 'bold'), bg="#e1f0f7")
        self.txt_charges.place(x=150, y=190, width=200)
        
        self.txt_description = Text(self.root, font=("goudy old style", 15, 'bold'), bg="#e1f0f7")
        self.txt_description.place(x=150, y=250, width=500, height=100)  
        
        # Button =========================
        
        self.btn_add=Button(self.root,text='Save',font=("goudy old style", 15, 'bold'), bg="#3BACB6", fg="black", cursor="hand2",command=self.add)
        self.btn_add.place(x=170, y=400,width=110, height=40)
        self.btn_update=Button(self.root,text='Update',font=("goudy old style", 15, 'bold'), bg="#B3E8E5", fg="black", cursor="hand2",command=self.update)
        self.btn_update.place(x=290, y=400,width=110, height=40)
        self.btn_delete=Button(self.root,text='Delete',font=("goudy old style", 15, 'bold'), bg="#3BACB6", fg="black", cursor="hand2",command=self.delete)
        self.btn_delete.place(x=410, y=400,width=110, height=40)
        self.btn_clear=Button(self.root,text='Clear',font=("goudy old style", 15, 'bold'), bg="#B3E8E5", fg="black", cursor="hand2",command=self.clear)
        self.btn_clear.place(x=530, y=400 ,width=110, height=40)
        
        
        # search ==========================
        self.var_search=StringVar()
        lbl_search = Label(self.root, text="Course Name:", font=("goudy old style", 15, 'bold'), bg="white").place(x=720, y=60)   
        txt_search_courseName = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, 'bold'), bg="#e1f0f7").place(x=870, y=60, width=180)
        btn_search=Button(self.root,text='search',font=("goudy old style", 15, 'bold'), bg="#3BACB6", fg="black", cursor="hand2",command=self.search).place(x=1070, y=60,width=120, height=28)    
        
        
        # content ==========================
        
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)
        
        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
       
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        # self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        # self.CourseTable.pack(fill=BOTH,expand=1)



        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = 'headings'
        # self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.column("cid",width=70)
        self.CourseTable.column("name",width=100)
        self.CourseTable.column("duration",width=100)
        self.CourseTable.column("charges",width=100)
        self.CourseTable.column("description",width=150)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        # self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        # self.show()
        footer = Label(self.root, text="Student Management System | GUJJU infotech | Contact Us: 7874273210",
                       font=("goudy old style", 12),  bg="#2F8F9D", fg="black")
        footer.pack(side=BOTTOM, fill=X)
# ================================================================================

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0',END)
        self.txt_courseName.config(state=NORMAL)




    def get_data(self,ev):
        self.txt_courseName.config(state='readonly')

        self.txt_courseName
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content["values"]
        print(row)
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        # self.var_course.set(row[4])
        self.txt_description.delete('1.0',END)
        self.txt_description.insert(END,row[4])

    def delete(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name should be required", parent=self.root)
            else:
                #    pass
                    cur.execute("select * from course where name=?", (self.var_course.get(),))
                    row = cur.fetchone()  # Fix: Call the method correctly
                    if row == None:  # Fix: Check if row exists
                        messagebox.showerror("Error", "Please select course from th list first!!!", parent=self.root)
                    else:
                        op=messagebox.askyesno("confirm","Do yo really want to delete??",parent=self.root)
                        if op==True:
                            cur.execute("delete from course where name=?",(self.var_course.get(),))
                            con.commit()
                            messagebox.showinfo("delete","course delete successfull !!",parent=self.root)
                            self.clear()
                            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")

    def add(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
       
        try:
           if self.var_course.get()=="":
               messagebox.showerror("Error","Course Name should be required", parent=self.root)
           else:
            #    pass
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()  # Fix: Call the method correctly
                if row is not None:  # Fix: Check if row exists
                    messagebox.showerror("Error", "Course Name Already exists!!!", parent=self.root)
                else:
                    cur.execute("insert into course (name, duration, charges, description) values (?, ?, ?, ?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END)  # Fix: Corrected field reference
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")
        finally:
            if 'con' in locals():
                con.close()
    
    

    def update(self):
            try:
                con = sqlite3.connect(database="sms.db")
                cur = con.cursor()

                if not self.var_course.get():
                    messagebox.showerror("Error", "Course Name is required", parent=self.root)
                    return

                # Check if course exists
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
            
                # Update course record
                cur.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?", (
                    self.var_duration.get(),
                    self.var_charges.get(),
                    self.txt_description.get("1.0", END).strip(),
                    self.var_course.get(),
                ))
                con.commit()
                messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
                self.show()

            except sqlite3.Error as ex:
                messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Unexpected error: {str(ex)}", parent=self.root)
            finally:
                if 'con' in locals():
                    con.close()
                    
                    
    def show(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course")
            rows = cur.fetchall()  # Fix: Call the method correctly
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")
    
    def search(self):
        con=sqlite3.connect(database="sms.db")
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()  # Fix: Call the method correctly
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")



    
if __name__ == "__main__":
    root = Tk()
    app = CourseClass(root)
    root.mainloop()
