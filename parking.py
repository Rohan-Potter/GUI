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
    database="parking"
)
cur=my_db.cursor(buffered=True)
## Application Window
app=tk.Tk()
app.geometry("1920x1200")
app.title("Parking Ticket")

##### Notebook ######
nb=ttk.Notebook(app)
page1=ttk.Frame(nb)
page2=ttk.Frame(nb)
nb.add(page1,text="Check-IN")
nb.grid(row=0,column=0)
nb.add(page2,text="Check-OUT")
nb.grid(row=0,column=1)
################################


################### CHECK-IN PAGE ##############################

check_in=ttk.LabelFrame(page1,text="Enter Details ")
check_in.grid(row=0,column=0,padx=600)


########### Buttons Functions ######################

def In():
    license_no=(car_no_var.get()).upper()
    Wheels=wheel_var.get()
    if license_no=='' or Wheels==0:
        m_box.showerror("No Data","Please fill all the data")
    else:
        query1=(f"SELECT * FROM ticket WHERE Wheels={Wheels} AND Parking_available='YES'")
        cur.execute(query1)
        info=cur.fetchone()
        query2=(f"UPDATE ticket SET  Parking_available='NO',License_No='{license_no}',Check_In_Date=CURDATE(),Check_In_Time=CURRENT_TIME() Where Parking_Code={info[0]}")
        cur.execute(query2)
        my_db.commit()
        m_box.showinfo("Successful",f" Floor {info[4]} Parking No {info[5]}")
        car_no_entry.delete(0,tk.END)

################# END FUNCTION ######################

#### Car lisence plate entry box and label #### 

car_no_label=ttk.Label(check_in,text="Enter Car Lisence Plate No: ")
car_no_label.grid(row=0,column=0,padx=10)

car_no_var=tk.StringVar()
car_no_entry=ttk.Entry(check_in,textvariable=car_no_var)
car_no_entry.grid(row=0,column=1,padx=10)
car_no_entry.focus()

####  No of wheels radio button ####

wheel_label=ttk.Label(check_in,text="Select No of wheels: ")
wheel_label.grid(row=1,column=0,pady=20)
    
wheel_var=tk.IntVar()

## 2 wheels
R1=tk.Radiobutton(check_in,text="2 wheels",variable=wheel_var,value=2)
R1.grid(row=2,column=0)
R1.configure(activebackground='gold')

## 4 Wheels
R2=tk.Radiobutton(check_in,text="4 wheels",variable=wheel_var,value=4)
R2.grid(row=3,column=0)
R2.configure(activebackground='gold')

### Submit button
submit_button=tk.Button(page1,text="Check-In",command=In)
submit_button.grid(row=1,column=0)
submit_button.configure(activebackground='orangered')

############################### Check-IN Page END ####################################

############################### CHech-Out Page #######################################

########### Buttons Functions ######################

def done():
    license_car=(car_license_var.get()).upper()
    query5=(f"UPDATE ticket SET Parking_available='YES',License_No=NULL,Check_In_Date=NULL,Check_In_Time=NULL,Check_Out_Date=NULL,Check_Out_Time=NULL WHERE License_No ='{license_car}' ")
    cur.execute(query5)
    my_db.commit()
    m_box.showinfo("Thank-You","Check Out Successful")


def out():
    car_license=(car_license_var.get()).upper()
    if car_license=="":
        m_box.showerror("No DATA","Please Enter the data to proceed")
    else:
        query3=(f"UPDATE ticket SET Check_Out_Date=CURDATE(),Check_Out_Time=CURRENT_TIME() Where License_No='{car_license}'")
        cur.execute(query3)
        my_db.commit()

        query4=(f"SELECT * FROM ticket WHERE License_No='{car_license}'")
        cur.execute(query4)
        details=cur.fetchone()

        if details==None:
            m_box.showerror("Error","License Plate Not Found")
            car_license_entry.delete(0,tk.END)

        else:
            ### Parking Detals 
            name=['Car License No','Check In Date','Check In Time','Check Out Date','Check Out Time','Total Parking Hours','Fare Per Hour']
            r=0
            for i in name:
                details_label_1=ttk.Label(label_details,text=i).grid(row=r,column=0,pady=5)
                r+=1
            Total_Fare_Label=ttk.Label(label_details,text='Total Fare')
            Total_Fare_Label.grid(row=7,column=0,pady=5)
            Total_Fare_Label.configure(foreground='red')

            Th=round(((details[9]-details[7]).seconds)/3600)
            if details[3]==4:
                fare=50
            else:
                fare=20
            value=[details[2],details[6],details[7],details[8],details[9],Th,fare]
            r=0
            for j in value:
                details_label_2=ttk.Label(label_details,text=j)
                details_label_2.grid(row=r,column=1,pady=5,padx=20)
                r+=1
                var_fare=Th*fare
                Fare_value=ttk.Label(label_details,text=var_fare)
                Fare_value.grid(row=7,column=1,pady=5)
                Fare_value.configure(foreground='red')

            ## confirm Button
            confirm_button=tk.Button(label_details,text="Confirm Check-Out",command=done)
            confirm_button.grid(row=8,columnspan=2)
            confirm_button.configure(foreground='red',activebackground='gold')
            




################### END FUNCTION ###################

check_out=ttk.LabelFrame(page2,text="Enter Details ")
check_out.grid(row=0,column=0,padx=600)

label_details=ttk.LabelFrame(page2,text="Parking Details")
label_details.grid(row=1,column=0,padx=600)

### Car license palte entry box and label

car_license_label=ttk.Label(check_out,text="Enter Car License Plate No :").grid(row=0,column=0,padx=10)
car_license_var=tk.StringVar()
car_license_entry=ttk.Entry(check_out,textvariable=car_license_var)
car_license_entry.grid(row=0,column=1,padx=10)
car_license_entry.focus()

### Check Out button

Check_Out_Button=tk.Button(check_out,text="Check Out Details",command=out)
Check_Out_Button.grid(row=1,columnspan=5,pady=10)
Check_Out_Button.configure(activebackground="red")



########################### END CHECK_OUT_PAGE ######################################
app.mainloop()



#################### APP END ######################