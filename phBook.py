import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox

class contact():
    def __init__(self,root):
        self.root = root
        self.root.title("Phone Book Management")
        self.root.configure(bg="pink")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, bg=self.clr(220,120,180),bd=3, relief="groove",text="Phone Book Management", font=("Arial",50,"bold"))
        title.pack(side="top",fill="x")

        # input frame

        inFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(180,200,120))
        inFrame.place(width=self.width/3, height=self.height-180, x=20, y=100)

        cityLbl = tk.Label(inFrame, text="City Name:",bg=self.clr(180,200,120),font=("Arial",15,"bold"))
        cityLbl.grid(row=0,column=0, padx=20,pady=30)
        self.cityIn = tk.Entry(inFrame,bd=2, font=("Arial",15),width=17)
        self.cityIn.grid(row=0,column=1,padx=10, pady=30)

        nameLbl = tk.Label(inFrame, text="Person Name:",bg=self.clr(180,200,120),font=("Arial",15,"bold"))
        nameLbl.grid(row=1,column=0, padx=20,pady=30)
        self.nameIn = tk.Entry(inFrame,bd=2, font=("Arial",15),width=17)
        self.nameIn.grid(row=1,column=1, padx=10, pady=30)

        phLbl = tk.Label(inFrame, text="Phone_No:",bg=self.clr(180,200,120),font=("Arial",15,"bold"))
        phLbl.grid(row=2, column=0, padx=20, pady=30)
        self.phIn = tk.Entry(inFrame,bd=2, font=("Arial",15),width=17)
        self.phIn.grid(row=2, column=1,padx=10, pady=30)

        addBtn = tk.Button(inFrame,command=self.insertFun, text="Add Number",bg="brown",fg="white", bd=2, relief="raised", font=("Arial",20,"bold"),width=20)
        addBtn.grid(row=3,column=0, padx=30, pady=100,columnspan=2)

        # detail Frame

        self.outFrame = tk.Frame(self.root, bd=4,relief="ridge", bg=self.clr(120,180,220))
        self.outFrame.place(width=self.width/2+150, height=self.height-180, x=self.width/3+30, y=100)

        optLbl = tk.Label(self.outFrame, text="Select:", bg=self.clr(120,180,220),font=("Arial",15,"bold"))
        optLbl.grid(row=0, column=0, padx=10, pady=15)

        self.combo= ttk.Combobox(self.outFrame, values=("New_York","California","Washington"),font=("Arial",15),width=13)
        self.combo.set("Select City")
        self.combo.grid(row=0, column=1, padx=10, pady=15)

        prsnLbl = tk.Label(self.outFrame, text="Person", bg=self.clr(120,180,220),font=("Arial",15,"bold"))
        prsnLbl.grid(row=0, column=2, padx=10, pady=15)
        self.prsnIn = tk.Entry(self.outFrame, width=14, font=("Arial",13),bd=2)
        self.prsnIn.grid(row=0, column=3, padx=10, pady=15)

        srchBtn = tk.Button(self.outFrame,command=self.searchFun, text="Search",bg="gray", width=6, bd=2, relief="raised",font=("Arial",18))
        srchBtn.grid(row=0, column=4, padx=10, pady=15)

        delBtn = tk.Button(self.outFrame,command=self.delFun, text="Delete",bg="gray", width=6, bd=2, relief="raised",font=("Arial",18))
        delBtn.grid(row=0, column=5, padx=10, pady=15)
        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.outFrame, bg="cyan", bd=4, relief="sunken")
        tabFrame.place(width=self.width/2+120, height=self.height-280, x=12, y=80)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(fill="x", side="bottom")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(fill="y", side="right")

        self.table = ttk.Treeview(tabFrame,columns=("cName","pName","phNo"), xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("cName", text="City_Name")
        self.table.heading("pName", text="Person_Name")
        self.table.heading("phNo", text="Phone_Number")
        self.table["show"]= "headings"

        self.table.column("cName", width=150)
        self.table.column("pName", width=150)
        self.table.column("phNo", width=200)

        self.table.pack(fill="both", expand=1)

    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def insertFun(self):
        cName = self.cityIn.get()
        pName = self.nameIn.get()
        ph = self.phIn.get()

        try:
            if cName and pName and ph:
                self.dbFun()
                query = f"insert into {cName}(cityName,pName,phNo) values(%s,%s,%s)"
                
                self.cur.execute(query,(cName,pName,ph))
                self.con.commit()
                tk.messagebox.showinfo("Success",f"Phone Number of {pName} is Added successfuly")
                query2 = f"select * from {cName} where pName=%s"
                self.cur.execute(query2,pName)
                row = self.cur.fetchone()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END, values=row)
                self.con.close()
                self.cityIn.delete(0,tk.END)
                self.nameIn.delete(0,tk.END)
                self.phIn.delete(0,tk.END)

            else:
                tk.messagebox.showerror("Error","Please Fill All Input Fields")

        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}")

    def searchFun(self):
        opt = self.combo.get()
        name = self.prsnIn.get()

        if opt and name:
            try:
                self.dbFun()
                query = f"select * from {opt} where pName=%s"
                self.cur.execute(query, name)
                data = self.cur.fetchone()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END,values=data)
                self.con.close()

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")
        
        else:
            tk.messagebox.showerror("Error","Fill All Fields")

    def delFun(self):
        opt = self.combo.get()
        name = self.prsnIn.get()

        if opt and name:
            try:
                self.dbFun()

                query= f"delete from {opt} where pName=%s"
                self.cur.execute(query,name)
                tk.messagebox.showinfo("Sucess",f"Number of {name} is Deleted")
                self.tabFun()
                self.table.delete(*self.table.get_children())

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")
        
        else:
            tk.messagebox.showerror("Error","Fill All Fields")


root = tk.Tk()
obj = contact(root)
root.mainloop()