import sqlite3
import mysql.connector


def create_db():
    try:

        con = sqlite3.connect(database="sms.db")
        cur = con.cursor()
        # Users table for login/registration (for admin users)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )""")
        con.commit()
        
        # Faculty table for faculty registration
        cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            contact TEXT NOT NULL,
            password TEXT NOT NULL,
            course TEXT NOT NULL
        )""")
        con.commit()
        
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS course (
            cid INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            duration TEXT, 
            charges INTEGER, 
            description TEXT
        )""")
        con.commit()
        
        
        
            # Create student table with foreign key
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student(
                    roll INTEGER PRIMARY KEY AUTOINCREMENT,
                    name text,
                    email text,
                    gender text,
                    dob DATE,
                    contact text,
                    admission DATE,
                    course INTEGER,
                    state text,
                    city text,
                    pin INTEGER,
                    address TEXT,
                    CONSTRAINT fk_course FOREIGN KEY (course) REFERENCES course(cid) ON DELETE CASCADE

                )
            """)
        con.commit()
           # Create result table with foreign key
        cur.execute("""
            CREATE TABLE IF NOT EXISTS result(
                rid INTEGER  PRIMARY KEY AUTOINCREMENT,
                roll INTEGER,
                name TEXT,
                course TEXT,
                marks_ob INTEGER,
                full_marks INTEGER,
                per REAL,
                CONSTRAINT fk_student FOREIGN KEY (roll) REFERENCES student(roll) ON DELETE CASCADE
            )
        """)
        con.commit()
        
       # Create attendance table with foreign key to course and student
        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                aid INTEGER PRIMARY KEY AUTOINCREMENT,
                roll INTEGER,
                date DATE,
                course INTEGER,
                status TEXT CHECK (status IN ('P', 'A')),
                CONSTRAINT fk_student FOREIGN KEY (roll) REFERENCES student(roll) ON DELETE CASCADE,
                CONSTRAINT fk_course FOREIGN KEY (course) REFERENCES course(cid) ON DELETE CASCADE,
                CONSTRAINT unique_attendance UNIQUE (roll, date, course)
            )
        """)
        con.commit()
        
         
        cur.execute("""
            CREATE TABLE IF NOT EXISTS register (
                reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                f_name TEXT,
                l_name TEXT,
                contact TEXT,
                email TEXT UNIQUE,
                question TEXT,
                answer TEXT,
                password TEXT
            )""")
        con.commit()
        

        con.close()  # Always close connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")

create_db()  # Ensure table is created before running the application



    
     