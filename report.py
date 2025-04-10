import sqlite3
import csv
import os
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime


class ReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("View Result Report")
        self.root.config(bg="white")
        self.root.update_idletasks()  # Ensure Tkinter initializes before setting geometry
        self.center_window()
        self.root.focus_force()

            
        # Title
        title = Label(self.root, text="Student Result Report !!", padx=10, compound=LEFT,
                      font=("goudy old style", 25, "bold"), bg="#B3E8E5", fg="black")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Search Bar
        self.var_search = StringVar()
        lbl_search = Label(self.root, text="Search Roll No:", font=("goudy old style", 14, "bold"), bg="white").place(x=180, y=80)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 14), bg="#e1f0f7").place(x=350, y=80, width=250)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 14, "bold"), bg="#17A2B8",
                           command=self.search).place(x=650, y=80, width=120)
        btn_show_all = Button(self.root, text="Show All", font=("goudy old style", 14, "bold"), bg="#17A2B8",
                             command=self.fetch_data).place(x=800, y=80, width=120)
        btn_export = Button(self.root, text="Generate Report", font=("goudy old style", 14, "bold"), bg="green", fg="black",
                           command=self.export_report).place(x=1100, y=80, width=200)
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 14, "bold"), bg="red", fg="black",
                           command=self.delete_data).place(x=950, y=80, width=120)

        # Result Table
        frame = Frame(self.root, bd=2, relief=RIDGE)
        frame.place(x=20, y=140, width=1400, height=500)

        scroll_x = Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame, orient=VERTICAL)

        self.result_table = ttk.Treeview(frame, columns=("rid", "roll", "name", "course", "marks", "full_marks", "per"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.result_table.xview)
        scroll_y.config(command=self.result_table.yview)

        self.result_table.heading("rid", text="Result ID")
        self.result_table.heading("roll", text="Roll No")
        self.result_table.heading("name", text="Name")
        self.result_table.heading("course", text="Course")
        self.result_table.heading("marks", text="Marks Obtained")
        self.result_table.heading("full_marks", text="Full Marks")
        self.result_table.heading("per", text="Percentage")
        self.result_table["show"] = "headings"

        self.result_table.column("rid", width=80, anchor=CENTER)
        self.result_table.column("roll", width=80, anchor=CENTER)
        self.result_table.column("name", width=150, anchor=CENTER)
        self.result_table.column("course", width=120, anchor=CENTER)
        self.result_table.column("marks", width=120, anchor=CENTER)
        self.result_table.column("full_marks", width=120, anchor=CENTER)
        self.result_table.column("per", width=120, anchor=CENTER)

        self.result_table.pack(fill=BOTH, expand=1)
        self.result_table.bind("<ButtonRelease-1>", self.get_cursor)
        # Style the table
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("goudy old style", 14, "bold"), background="#B3E8E5", foreground="black")
        style.configure("Treeview", font=("goudy old style", 12), rowheight=25)
        self.fetch_data()

        # Footer
        footer = Label(self.root, text="Student Management System | GUJJU infotech | Contact Us: 7874273210",
                       font=("goudy old style", 12),  bg="#2F8F9D", fg="black")
        footer.pack(side=BOTTOM, fill=X)
        
        
        
        
    def fetch_data(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT rid, roll, name, course, marks_ob, full_marks, per FROM result")
            rows = cur.fetchall()
            print("Fetched rows:", rows)  # Debug print of raw data
            self.result_table.delete(*self.result_table.get_children())
            for row in rows:
                rid, roll, name, course, marks_ob, full_marks, per = row
                # Use stored percentage if valid, otherwise calculate
                if per is not None and per != "N/A" and isinstance(per, (int, float)):
                    display_per = f"{per:.2f}%"
                else:
                    display_per = self.calculate_percentage(marks_ob, full_marks)
                self.result_table.insert("", END, values=(rid, roll, name, course, marks_ob, full_marks, display_per))
        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Error fetching data: {str(ex)}")
        finally:
            con.close()


    def search(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT rid, roll, name, course, marks_ob, full_marks, per FROM result WHERE roll=?", (self.var_search.get(),))
            rows = cur.fetchall()
            print("Search results:", rows)  # Debug print
            if rows:
                self.result_table.delete(*self.result_table.get_children())
                for row in rows:
                    rid, roll, name, course, marks_ob, full_marks, per = row
                    if per is not None and per != "N/A" and isinstance(per, (int, float)):
                        display_per = f"{per:.2f}%"
                    else:
                        display_per = self.calculate_percentage(marks_ob, full_marks)
                    self.result_table.insert("", END, values=(rid, roll, name, course, marks_ob, full_marks, display_per))
            else:
                messagebox.showerror("Error", "No record found")
                self.fetch_data()  # Restore all data if no match
        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Error searching data: {str(ex)}")
        finally:
            con.close()
            
    def get_cursor(self, event):
        cursor_row = self.result_table.focus()
        contents = self.result_table.item(cursor_row)
        row = contents['values']
        if row:
            self.var_search.set(row[1])  # Set the roll number in the search field

    def delete_data(self):
        if not self.var_search.get():
            messagebox.showerror("Error", "Please select a record to delete or enter a roll number")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            try:
                con = sqlite3.connect(database="sms.db")
                cur = con.cursor()
                cur.execute("DELETE FROM result WHERE roll=?", (self.var_search.get(),))
                con.commit()
                messagebox.showinfo("Success", "Record Deleted Successfully")
                self.fetch_data()
            except sqlite3.Error as ex:
                messagebox.showerror("Database Error", f"Error deleting data: {str(ex)}")
            finally:
                con.close()
                
    def export_report(self):
        try:
            con = sqlite3.connect(database="sms.db")
            cur = con.cursor()
            cur.execute("SELECT rid, roll, name, course, marks_ob, full_marks, per FROM result")
            rows = cur.fetchall()
            print("Export rows:", rows)  # Debug print
            if rows:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"student_results_{timestamp}.csv"
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Result ID", "Roll No", "Name", "Course", "Marks Obtained", "Full Marks", "Percentage"])
                    for row in rows:
                        rid, roll, name, course, marks_ob, full_marks, per = row
                        if per is not None and per != "N/A" and isinstance(per, (int, float)):
                            display_per = f"{per:.2f}%"
                        else:
                            display_per = self.calculate_percentage(marks_ob, full_marks)
                        writer.writerow([rid, roll, name, course, marks_ob, full_marks, display_per])
                messagebox.showinfo("Success", f"Report generated as '{filename}'")
            else:
                messagebox.showerror("Error", "No data available to export")
        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Error exporting data: {str(ex)}")
        except IOError as ex:
            messagebox.showerror("File Error", f"Error writing file: {str(ex)}")
        finally:
            con.close()

   
    def center_window(self, width=1450, height=700):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")

if __name__ == "__main__":
    root = Tk()
    obj = ReportClass(root)
    root.mainloop()