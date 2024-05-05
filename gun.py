from tkinter import *
from tkinter import messagebox
import mysql.connector as mc
from PIL import Image, ImageTk

con = mc.connect(host="localhost", user="root", passwd="vishal", database="vishal")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS Pilot_details (
    PILOT_ID INT AUTO_INCREMENT PRIMARY KEY,
    PILOT_NAME VARCHAR(255) NOT NULL,
    DATE_OF_BIRTH DATE,
    ADDRESS VARCHAR(255),
    VALIDITY_DATE DATE,
    BLOOD_GROUP VARCHAR(10),
    BATCH_NO VARCHAR(20),
    FATHER_NAME VARCHAR(255),
    PHONE_NO VARCHAR(15)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Project (
    PROJECT_ID INT AUTO_INCREMENT PRIMARY KEY,
    DATE DATE,
    Reg_NO VARCHAR(20),
    PILOT_NAME VARCHAR(255),
    AIRCRAFT_TYPE VARCHAR(255),
    AIRCRAFT_IDENT VARCHAR(255),
    FLIGHT_FROM VARCHAR(255),
    FLIGHT_TO VARCHAR(255),
    REMARKS_AND_ENDORSEMENTS VARCHAR(255)
)
""")
def login():
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()

        # Check credentials
        if username == "admin" and password == "admin":
            login_window.destroy()  # Close login window
            main_page()  # Show main application window
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.config(bg='Orange')
    login_window.resizable(0,0)
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x_coordinate = (screen_width - 300) // 2
    y_coordinate = (screen_height - 200) // 2
    login_window.geometry("+{}+{}".format(x_coordinate, y_coordinate))
    
    
    
    label_username = Label(login_window, text="Username:", font=('Arial', 12), bg='light grey')
    label_username.pack(pady=5)
    entry_username = Entry(login_window, font='12')
    entry_username.pack()

    label_password = Label(login_window, text="Password:", font=('Arial', 12), bg='light grey')
    label_password.pack(pady=5)
    entry_password = Entry(login_window, show="*", font='12')
    entry_password.pack()

    login_button = Button(login_window, text="Login", command=authenticate, font=('Arial', 12), bg='light blue')
    login_button.pack(pady=10)

    login_window.mainloop()

'''def set_background(window, image_path):
    img = Image.open(image_path)
    
    # Resize the image to fit the window size
    img = img.resize((window.winfo_width(), window.winfo_height()))
    
    # Convert the Image object to a Tkinter-compatible photo image
    photo = ImageTk.PhotoImage(img)
    
    # Create a label with the photo image
    label = Label(window, image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection
    
    # Place the label in the window
    label.place(x=0, y=0, relwidth=1, relheight=1)'''
    
def reset(entries):
    for entry in entries:
        entry.delete(0, END)

def insert_pilot_details():
    def submit(pilot_name, date_of_birth, address, validity_date, blood_group, batch_no, father_name, phone_no):
        query = "INSERT INTO Pilot_details (PILOT_NAME, DATE_OF_BIRTH, ADDRESS, VALIDITY_DATE, BLOOD_GROUP, BATCH_NO, FATHER_NAME, PHONE_NO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (pilot_name, date_of_birth, address, validity_date, blood_group, batch_no, father_name, phone_no)

        cur.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", "Data inserted successfully")

    b = Tk()
    b.title("Pilot Details")
    b.geometry("600x500")
    b.config(bg='light blue')

    labels = ['PILOT_NAME', 'DATE_OF_BIRTH', 'ADDRESS', 'VALIDITY_DATE', 'BLOOD_GROUP', 'BATCH_NO', 'FATHER_NAME', 'PHONE_NO']
    entries = []
    
    for i, label_text in enumerate(labels):
        lbl_label = Label(b, text=label_text, font=('Algerian', 10))
        lbl_label.place(x=100, y=50+i*30)
        entry = Entry(b, font='16')
        entry.place(x=350, y=50+i*30)
        entries.append(entry)

    login_btn = Button(b, text='RESET', command=lambda: reset(entries), bd=1)
    login_btn.place(x=100, y=400)
    login_btn = Button(b, text='SUBMIT', command=lambda: submit(*[entry.get() for entry in entries]), bd=1)
    login_btn.place(x=200, y=400)

    b.mainloop()


def update_pilot_details():
    def submit():
        Phone_No = e1.get()
        field = e2.get()
        new_value = e3.get()

        if field not in ['PILOT_NAME', 'DATE_OF_BIRTH', 'ADDRESS', 'VALIDITY_DATE', 'BLOOD_GROUP', 'BATCH_NO', 'FATHER_NAME', 'PHONE_NO']:
            messagebox.showerror("Error", "Invalid field")
            return

        query = f"UPDATE Pilot_details SET {field} = %s WHERE PHONE_NO = %s"
        values = (new_value, Phone_No)

        cur.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", "Data updated successfully")

    b = Tk()
    b.title("Update Pilot Details")
    b.geometry("400x250")
    b.config(bg='light blue')

    lbl_Phone_no = Label(b, text="Enter Phone_NO ()", font=('Algerian', 10))
    lbl_Phone_no.place(x=50, y=50)
    e1 = Entry(b, font='16')
    e1.place(x=300, y=50)

    lbl_field = Label(b, text="Enter field to update", font=('Algerian', 10))
    lbl_field.place(x=50, y=100)
    e2 = Entry(b, font='16')
    e2.place(x=300, y=100)

    lbl_new_value = Label(b, text="Enter new value", font=('Algerian', 10))
    lbl_new_value.place(x=50, y=150)
    e3 = Entry(b, font='16')
    e3.place(x=300, y=150)

    login_btn = Button(b, text='SUBMIT', command=submit, bd=1)
    login_btn.place(x=200, y=200)

    b.mainloop()

def delete_pilot_details():
    def submit():
        phone_no = e2.get()

        query = "DELETE FROM Pilot_details WHERE Phone_No = %s"
        values = (phone_no,)

        cur.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", "Data deleted successfully")

    b = Tk()
    b.title("Delete Pilot Details")
    b.geometry("400x200")
    b.config(bg='light green')

    lbl_pilot_name = Label(b, text="Enter Pilot's Phone_NO to delete", font=('Algerian', 10))
    lbl_pilot_name.place(x=50, y=50)
    e2 = Entry(b, font='16')
    e2.place(x=300, y=50)

    login_btn = Button(b, text='SUBMIT', command=submit, bd=1)
    login_btn.place(x=200, y=100)

    b.mainloop()

def select_pilot_details():
    def submit():
        phone_no = e2.get()

        query = "SELECT * FROM Pilot_details WHERE phone_no = %s"
        values = (phone_no,)

        cur.execute(query, values)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                messagebox.showinfo("Pilot Details", f"PILOT_NAME: {row[0]}\nDATE_OF_BIRTH: {row[1]}\nADDRESS: {row[2]}\nVALIDITY_DATE: {row[3]}\nBLOOD_GROUP: {row[4]}\nBATCH_NO: {row[5]}\nFATHER_NAME: {row[6]}\nPHONE_NO: {row[7]}")
        else:
            messagebox.showinfo("Pilot Details", "No pilot found with the provided Phone_No")

    b = Tk()
    b.title("Select Pilot Details")
    b.geometry("400x200")
    b.config(bg='light green')

    lbl_pilot_name = Label(b, text="Enter Pilot's Phone_No to Fetch", font=('Algerian', 10))
    lbl_pilot_name.place(x=50, y=50)
    e2 = Entry(b, font='16')
    e2.place(x=300, y=50)

    login_btn = Button(b, text='SUBMIT', command=submit, bd=1)
    login_btn.place(x=200, y=100)

    b.mainloop()

def insert_project_details():
    def submit(date, reg_no, pilot_name, aircraft_type, aircraft_ident, flight_from, flight_to, remarks_and_endorsements):
        query = "INSERT INTO Project (DATE, Reg_NO, PILOT_NAME, AIRCRAFT_TYPE, AIRCRAFT_IDENT, FLIGHT_FROM, FLIGHT_TO, REMARKS_AND_ENDORSEMENTS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (date, reg_no, pilot_name, aircraft_type, aircraft_ident, flight_from, flight_to, remarks_and_endorsements)

        cur.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", "Data inserted successfully")

    b = Tk()
    b.title("Project Details")
    b.geometry("600x500")
    b.config(bg='light blue')

    labels = ['DATE', 'Reg_NO', 'PILOT_NAME', 'AIRCRAFT_TYPE', 'AIRCRAFT_IDENT', 'FLIGHT_FROM', 'FLIGHT_TO', 'REMARKS_AND_ENDORSEMENTS']
    entries = []
    
    for i, label_text in enumerate(labels):
        lbl_label = Label(b, text=label_text, font=('Algerian', 10))
        lbl_label.place(x=100, y=50+i*30)
        entry = Entry(b, font='16')
        entry.place(x=350, y=50+i*30)
        entries.append(entry)

    login_btn = Button(b, text='RESET', command=lambda: reset(entries), bd=1)
    login_btn.place(x=100, y=400)
    login_btn = Button(b, text='SUBMIT', command=lambda: submit(*[entry.get() for entry in entries]), bd=1)
    login_btn.place(x=200, y=400)

    b.mainloop()

def update_project_details():
    def submit():
        reg_no = e1.get()
        field = e2.get()
        new_value = e3.get()

        if field not in ['DATE', 'PILOT_NAME', 'AIRCRAFT_TYPE', 'AIRCRAFT_IDENT', 'FLIGHT_FROM', 'FLIGHT_TO', 'REMARKS_AND_ENDORSEMENTS']:
            messagebox.showerror("Error", "Invalid field")
            return

        query = f"UPDATE Project SET {field} = %s WHERE Reg_NO = %s"
        values = (new_value, reg_no)

        cur.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", "Data updated successfully")

    b = Tk()
    b.title("Update Project Details")
    b.geometry("400x250")
    b.config(bg='light green')

    lbl_reg_no = Label(b, text="Enter Reg_NO ()", font=('Algerian', 10))
    lbl_reg_no.place(x=50, y=50)
    e1 = Entry(b, font='16')
    e1.place(x=300, y=50)

    lbl_field = Label(b, text="Enter field to update", font=('Algerian', 10))
    lbl_field.place(x=50, y=100)
    e2 = Entry(b, font='16')
    e2.place(x=300, y=100)

    lbl_new_value = Label(b, text="Enter new value", font=('Algerian', 10))
    lbl_new_value.place(x=50, y=150)
    e3 = Entry(b, font='16')
    e3.place(x=300, y=150)

    login_btn = Button(b, text='SUBMIT', command=submit, bd=1)
    login_btn.place(x=200, y=200)

    b.mainloop()

def delete_project_details():
    def submit():
        date = e2.get()
        reg_no = e3.get()

        query = "DELETE FROM Project WHERE DATE = %s AND Reg_NO = %s"
        values = (date, reg_no)

        cur.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", "Data deleted successfully")

    b = Tk()
    b.title("Delete Project Details")
    b.geometry("400x200")
    b.config(bg='light green')

    lbl_date = Label(b, text="Enter DATE ()", font=('Algerian', 10))
    lbl_date.place(x=50, y=50)
    e2 = Entry(b, font='16')
    e2.place(x=300, y=50)

    lbl_reg_no = Label(b, text="Enter Reg_NO ()", font=('Algerian', 10))
    lbl_reg_no.place(x=50, y=100)
    e3 = Entry(b, font='16')
    e3.place(x=300, y=100)

    login_btn = Button(b, text='SUBMIT', command=submit, bd=1)
    login_btn.place(x=200, y=150)

    b.mainloop()

def select_project_details():
    def submit():
        date = e2.get()
        reg_no = e3.get()

        query = "SELECT * FROM Project WHERE DATE = %s AND Reg_NO = %s"
        values = (date, reg_no)

        cur.execute(query, values)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                messagebox.showinfo("Project Details", f"DATE: {row[0]}\nReg_NO: {row[1]}\nPILOT_NAME: {row[2]}\nAIRCRAFT_TYPE: {row[3]}\nAIRCRAFT_IDENT: {row[4]}\nFLIGHT_FROM: {row[5]}\nFLIGHT_TO: {row[6]}\nREMARKS_AND_ENDORSEMENTS: {row[7]}")
        else:
            messagebox.showinfo("Project Details", "No project found with the provided DATE and Reg_NO")

    b = Tk()
    b.title("Select Project Details")
    b.geometry("400x250")
    b.config(bg='light green')

    lbl_date = Label(b, text="Enter DATE ()", font=('Algerian', 10))
    lbl_date.place(x=50, y=50)
    e2 = Entry(b, font='16')
    e2.place(x=300, y=50)

    lbl_reg_no = Label(b, text="Enter Reg_NO ()", font=('Algerian', 10))
    lbl_reg_no.place(x=50, y=100)
    e3 = Entry(b, font='16')
    e3.place(x=300, y=100)

    login_btn = Button(b, text='SUBMIT', command=submit, bd=1)
    login_btn.place(x=200, y=150)

    b.mainloop()


from tkinter import *
from tkinter import messagebox
import mysql.connector as mc
from PIL import Image, ImageTk

def main_page():
    window = Tk()
    window.title("Aircraft Management System")
    window.geometry("600x600+300+50")
    window.resizable(0, 0)
    window.config(bg='black')
    label = Label(window, text="Welcome to Aircraft Management System", font=("Arial", 20), bg='black', fg='white')
    label.pack(pady=20)
    label.place(x=45, y=50)
    b=Button(window, text="Pilot Management", command=pilot_management,font=("Arial", 15), bg='lemonchiffon')
    b.pack(pady=10)
    b.place(x=200, y=200)
    n=Button(window, text="Flight Management", command=project_management, font=("Arial", 15), bg='lemonchiffon')
    n.pack(pady=10)
    n.place(x=195, y=300)
    window.mainloop()
main_page()

def pilot_management():
    pilot_window = Tk()
    pilot_window.title("Pilot Management")
    pilot_window.geometry("600x600+300+50")
    pilot_window.resizable(0, 0)
    pilot_window.config(bg='light blue')

    Label(pilot_window, text="Pilot Management", font=("Arial", 20), bg='light blue').pack(pady=20)

    Button(pilot_window, text="Insert Pilot Details", font=("Arial", 15), command=insert_pilot_details, bg='lemonchiffon').pack(pady=10)
    Button(pilot_window, text="Update Pilot Details", font=("Arial", 15), command=update_pilot_details, bg='lemonchiffon').pack(pady=10)
    Button(pilot_window, text="Delete Pilot Details", font=("Arial", 15), command=delete_pilot_details, bg='lemonchiffon').pack(pady=10)
    Button(pilot_window, text="Select Pilot Details", font=("Arial", 15), command=select_pilot_details, bg='lemonchiffon').pack(pady=10)

    pilot_window.mainloop()

def project_management():
    project_window = Tk()
    project_window.title("Project Management")
    project_window.geometry("600x600+300+50")
    project_window.resizable(0, 0)
    project_window.config(bg='light green')

    Label(project_window, text="Project Management", font=("Arial", 20), bg='light green').pack(pady=20)

    Button(project_window, text="Insert Project Details", font=("Arial", 15), command=insert_project_details, bg='lemonchiffon').pack(pady=10)
    Button(project_window, text="Update Project Details", font=("Arial", 15), command=update_project_details, bg='lemonchiffon').pack(pady=10)
    Button(project_window, text="Delete Project Details", font=("Arial", 15), command=delete_project_details, bg='lemonchiffon').pack(pady=10)
    Button(project_window, text="Select Project Details", font=("Arial", 15), command=select_project_details, bg='lemonchiffon').pack(pady=10)

    project_window.mainloop()

if __name__ == "__main__":
    login()  # Show login window first