## Modules
import mysql.connector
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box

## Estabilishig Connection
my_db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rs20111998",
    database="library"
)
cur=my_db.cursor()
## Application Window
main_application=tk.Tk()
main_application.geometry("1920x1200")
main_application.title("Library Database")
################################################## Issue page #######################################################
nb=ttk.Notebook(main_application)
issue=ttk.Frame(nb)
nb.add(issue,text="issue")
nb.grid(row=0,column=0)
##### label_frame1
label_frame1=ttk.LabelFrame(issue,text="Enter Book Code to check availability :")
label_frame1.grid(row=0,column=0,padx=550,pady=50)
##### Book code label and entry box
book_code_label=ttk.Label(label_frame1,text="Please Enter Book Code :")
book_code_label.grid(row=0,column=0,pady=5,sticky=tk.W)
book_code_var=tk.IntVar()
book_code_entry=ttk.Entry(label_frame1,textvariable=book_code_var)
book_code_entry.grid(row=0,column=1,padx=5)
book_code_entry.delete(0,tk.END)
book_code_entry.focus()


##### responce
def responce(result):
    label_frame2=ttk.LabelFrame(issue,text="")
    label_frame2.grid(row=1,column=0)
    ###
    column_label=ttk.Label(label_frame2,)
    column_label.pack(expand=True,fill=tk.X)
    ## for headings
    a=0
    t=("Book Code","Book Name","Author Name"," ISBN no.","Status","Student Id","Issue Date","Return Date")
    for i in t:
        headings=ttk.Label(column_label,text=i).grid(row=0,column=a,padx=20)
        a +=1
    ## For result
    a=0
    for i in result:
        headings1=ttk.Label(column_label,text=i).grid(row=1,column=a,padx=20,pady=5)
        a+=1
    ## Issue btn and functionality
    def booked():
        stu_id=student_id_var.get()
        book_code=book_code_var.get()
        q=datetime.datetime.now()+datetime.timedelta(days=10)
        r=q.strftime("%x")
        query2=f"UPDATE data SET status='unavailable', stu_id={stu_id}, issue_date=CURDATE(), return_date=DATE_ADD(CURDATE(),INTERVAL 10 DAY) WHERE book_code={book_code}"
        cur.execute(query2)
        my_db.commit()
        m=m_box.showinfo("Book Issued",f"Your return date is {r}")
        

    ## student Entery box  and label
    student_id_label=ttk.Label(column_label,text="Enter the Student id :").grid(row=2,column=0,sticky=tk.W,pady=20)
    student_id_var=tk.IntVar()
    student_id_entry=ttk.Entry(column_label,textvariable=student_id_var,width=20,)
    student_id_entry.grid(row=2,column=1,padx=5,pady=20)
    student_id_entry.delete(0,tk.END)
    ## Issue btn
    issue_btn=tk.Button(column_label,text="Issue",command=booked)
    issue_btn.configure(foreground="blue")
    issue_btn.grid(row=2,column=2)
### Check Button Functionality
def check():
    book_code=book_code_var.get()
    query1=f"SELECT * FROM data WHERE book_code={book_code}"
    cur.execute(query1)
    result=cur.fetchone()
    try:
        if result[4]=="available":
            responce(result)
        elif result[4]=="unavailable":
            m_box.showinfo("Can't Issue","Book is Pre-Issued")
    except TypeError:
        m_box.showerror("Code Error","You have entered wrong code")
        book_code_entry.delete(0,tk.END)
    

check_btn=tk.Button(label_frame1,text="Check",command=check)
check_btn.configure(foreground="Blue")
check_btn.grid(row=1,column=0)

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& END ISSUE PAGE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#

################################################## RETURN PAGE ######################################################
retn=ttk.Frame(nb)
nb.add(retn,text="return")
nb.grid(row=0,column=1)

######### Return frame
label_frame3=ttk.LabelFrame(retn,text="Enter the details below ")
label_frame3.grid(row=0,column=0,padx=550,pady=50)
################
### Return label and entry box
return_label=ttk.Label(label_frame3,text="Enter the book code :").grid(row=0,column=0,sticky=tk.W,pady=15)
return_box_var=tk.IntVar()
return_entry_box=ttk.Entry(label_frame3,textvariable=return_box_var)
return_entry_box.grid(row=0,column=1,padx=5)
return_entry_box.delete(0,tk.END)

## Responce2 function
def responce2(info):
    label_frame4=ttk.LabelFrame(retn,text="")
    label_frame4.grid(row=1,column=0)
    ###
    column_label2=ttk.Label(label_frame4,)
    column_label2.pack(expand=True,fill=tk.X)
    ## for headings
    z=0
    q=("Book Code","Book Name","Author Name"," ISBN no.","Status","Student Id","Issue Date","Return Date")
    for j in q:
        headings3=ttk.Label(column_label2,text=j).grid(row=0,column=z,padx=20)
        z +=1
    ## For result
    z=0
    for j in info:
        headings4=ttk.Label(column_label2,text=j).grid(row=1,column=z,padx=20,pady=5)
        z+=1
    
    ### submit btn  and functionality ####
    def submit():
        book_id=return_box_var.get()
        query4=f"UPDATE data SET status='available',stu_id=0,issue_date='-',return_date='-' WHERE book_code={book_id} "
        cur.execute(query4)
        my_db.commit()
        m_box.showinfo("Thank-you","Return Successfully!!")
    
    ## Submit btn
    submit_btn=tk.Button(column_label2,text="Return",command=submit)
    submit_btn.configure(foreground="Red")
    submit_btn.grid(row=2,column=2)


## return button and functionality
def confirm():
    book_code2=return_box_var.get()
    query3=f"SELECT * FROM data WHERE book_code={book_code2}"
    cur.execute(query3)
    info=cur.fetchone()
    try:
        if info[4]=="unavailable":
            responce2(info)
        elif info[4]=="available":
            m_box.showinfo("Error","Please!! Issue book first")
    except TypeError:
        m_box.showerror("Code Eorror","Please!! Re-Enter the Code")
        return_entry_box.delete(0,tk.END)

return_btn=tk.Button(label_frame3,text="Confirm",command=confirm)
return_btn.configure(foreground="blue")
return_btn.grid(row=2,column=0)

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& End Return page &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
main_application.mainloop()