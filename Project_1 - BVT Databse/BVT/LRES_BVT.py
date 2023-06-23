#cd "C:\Users\User\Dropbox\Python\LRNetworks"
#cd "C:\Users\NIDS\Dropbox\Python\LRNetworks"
#cd "\\researchdata.uct.ac.za\LRES\Survey_Assistants\LRES_Database\PyDatabase"

from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
import mysql.connector
import csv
import sqlite3
from sqlalchemy import create_engine
from PIL import ImageTk, Image
import datetime
from tkcalendar import Calendar, DateEntry
import openpyxl
from tkinter.ttk import Progressbar
from LRESTreeviewDB import Database
#from LRESTreeviewDB_Com import Database_Com
#from LRESTreeviewDB_Land import Database_Land
from Toggle_Frame import ToggledFrame
import os



db = Database('lres_tree.db')
#dbc = Database_Com('lres_tree.db')
#dbl = Database_Land('lres_tree.db')
sd = '//researchdata.uct.ac.za/LRES/Survey_Assistants/LRES_Database/PyDatabase/'


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    

def center(win, width, height):
    win.update_idletasks()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


#img_refresh = Image.open("{}".format(sd) + "refresh2.png")
#img_refresh = Image.open(resource_path("refresh2.png"))
#resized_refresh = img_refresh.resize((18,16), Image.ANTIALIAS)
#new_refresh = ImageTk.PhotoImage(resized_refresh)


class StartApp:
    """This will check if database is already connected or not
    if already connected then login form will popup otherwise
    it will ask to connect0 the database by calling connect database
    class"""
    current_user = []
    current_user_level = []
    a='#249794'
    def __init__(self, window):
        self.window = window
       
        
        self.window.width_of_window = 500
        self.window.height_of_window = 330
        self.window.screen_width = self.window.winfo_screenwidth()
        self.window.screen_height = self.window.winfo_screenheight()
        self.window.x_coordinate = (self.window.screen_width/2)-(self.window.width_of_window/2)
        self.window.y_coordinate = (self.window.screen_height/2)-(self.window.height_of_window/2)
        self.window.geometry("%dx%d+%d+%d" %(self.window.width_of_window,self.window.height_of_window,self.window.x_coordinate,self.window.y_coordinate))
        
        
        #self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
        self.window.overrideredirect(1)
        #center(self.window, width=500, height=330)

        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')

        self.txtusername=Entry(self.window,width=28,fg='white', bg='#EFAD29',bd=0)
        self.txtusername.place(x=0,y=28)

        self.progress=Progressbar(self.window,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=520,mode='determinate',)
        self.progress.place(x=-10,y=315)

        self.mainframe=Frame(self.window,width=500,height=321,bg=StartApp.a)
        self.mainframe.place(x=0,y=0)  #249794

        self.loginpage()
        Button(self.mainframe,width=17,height=0,text='L O G I N', command=self.loginpage, pady=4,border=0,bg=StartApp.a,fg='white',activebackground=StartApp.a,activeforeground='white').place(x=250,y=0)
        Button(self.mainframe,width=17,height=0,text='R E S E T',pady=4,border=0,bg='#EFAD29',fg='white',activebackground='#EFAD29',activeforeground='white').place(x=380,y=0)

    def loginpage(self):
        self.logframe=Frame(self.mainframe,width=500,height=293,bg=StartApp.a)
        self.logframe.place(x=0,y=28)  #249794

        ######## Label

        self.l1=Label(self.logframe,text='LRES',fg='white',bg=StartApp.a)
        self.lst1=('Calibri (Body)',18,'bold')
        self.l1.config(font=self.lst1)
        self.l1.place(x=50,y=40)

        self.l2=Label(self.logframe,text='CAPTURE',fg='white',bg=StartApp.a)
        self.lst2=('Calibri (Body)',18)
        self.l2.config(font=self.lst2)
        self.l2.place(x=122,y=42)

        self.l3=Label(self.logframe,text='BENEFICIARY VERIFICATION TRACING',fg='white',bg=StartApp.a)
        self.lst3=('Calibri (Body)',13)
        self.l3.config(font=self.lst3)
        self.l3.place(x=50,y=70)

        #self.l4=Label(self.window,image=self.new_logo)
        #self.l4.place(x=50,y=130)
                #entrybox for username

        self.lst4=('Calibri (Body)',9)
        self.label_username = Label(self.logframe, text = "Username")
        self.label_username.config(font=self.lst4)
        self.label_username.place(x=250,y=120)
        self.label_password = Label(self.logframe, text = "Password")
        self.label_password.config(font=self.lst4)
        self.label_password.place(x=250,y=180)

        self.entry_username = Entry(self.logframe)
        self.entry_username.config(font=self.lst4)
        self.entry_username.place(x=250,y=150)

        self.entry_password = Entry(self.logframe, show="*")
        self.entry_password.config(font=self.lst4)
        self.entry_password.place(x=250,y=210)


        self.b2 = Button(self.logframe, text="Exit", width=10, height=1, command=self.window.quit, border=0,fg=StartApp.a,bg='white')
        self.b2.place(x=250,y=240)
        self.b1=Button(self.logframe,width=10,height=1,text='Login',command=self.login,border=0,fg=StartApp.a,bg='white')
        self.b1.place(x=350,y=240)
        self.elogin = self.window.bind('<Return>', self.enter)

        #self.b2.grid(row=2, column=0, pady=10, sticky=W)
        #self.progress.place(x=-10,y=315)

    def resetpage(self):
        #self.mainframe.configure(bg='#EFAD29')
        self.resframe=Frame(self.mainframe,width=500,height=293,bg='#EFAD29')
        self.resframe.place(x=0,y=28)

        def on_enter(e):
            self.reset_password.delete(0,'end')
        def on_leave(e):
            if self.reset_password.get()=='':
                self.reset_password.insert(0,'enter new password')

        #entrybox for username
        self.reset_password =Entry(self.resframe,width=46,fg='grey')
        self.reset_password.config(font=('Calibri (Body)',9))
        self.reset_password.bind("<FocusIn>", on_enter)
        self.reset_password.bind("<FocusOut>", on_leave)
        self.reset_password.insert(0,'enter password')
        self.reset_password.place(x=90,y=110-28)

        def on_enter(e):
            self.check_password.delete(0,'end')
        def on_leave(e):
            if self.check_password.get()=='':
                self.check_password.insert(0,'confirm new password')

        #entrybox for password
        self.check_password =Entry(self.resframe,width=46,fg='grey')
        self.check_password.config(font=('Calibri (Body)',9))
        self.check_password.bind("<FocusIn>", on_enter)
        self.check_password.bind("<FocusOut>", on_leave)
        self.check_password.insert(0,'confirm password')
        self.check_password.place(x=90,y=160-28)

        self.b4 = Button(self.resframe,width=10,height=0,text='Back',command=self.loginpage,border=0,fg='#EFAD29',bg='white')
        self.b4.place(x=160,y=214-28)
        self.b3 = Button(self.resframe,width=10,height=0,text='Reset',command=self.reset,border=0,fg='#EFAD29',bg='white')
        self.b3.place(x=260,y=214-28)
        self.window.unbind('<Return>', self.elogin)


    def enter(self, e):
        if self.entry_username.get() == ""  or self.entry_password.get() == "":
            messagebox.showerror("Login Error", "Please enter Username and Password.")
            return False
        else:
            self.login()

    def login(self):
        if self.entry_username.get() == ""  or self.entry_password.get() == "":
            messagebox.showerror("Login Error", "Please enter Username and Password.")
            return False
        else:
            self.user = StringVar()
            self.userlevel = IntVar()
            self.username = self.entry_username.get()
            self.password = self.entry_password.get()

            try:
                if str(db.userdict[self.username]['UserPassword']) == str(self.password) and str(db.userdict[self.username]['UserPassword'])  != "12345":
                    #aut64h1 = True
                    self.user = db.userdict[self.username]['Username']
                    self.userlevel = db.userdict[self.username]['UserSecurity']
                    StartApp.current_user.clear()
                    StartApp.current_user_level.clear()
                    StartApp.current_user.append(self.user)
                    StartApp.current_user_level.append(self.userlevel)

                    
                    messagebox.showinfo("Login Successful", f"Welcome {self.user}.")
                    self.bar()

                else:
                    if str(db.userdict[self.username]['UserPassword']) == str(self.password) and str(self.password) == "12345":
                        messagebox.showinfo("Password Reset", "Please change password.")
                        self.txtusername.insert(0,str(self.username))
                        self.resetpage()

                    else:
                        messagebox.showerror("Login Error", "Incorrect Username or Password.")
                        return False

            except KeyError:
                    messagebox.showerror("Login Error", "Incorrect Username or Password.")
                    return False


    def reset(self):
        if self.reset_password.get() == "" or self.reset_password.get() == "enter password"  or self.check_password.get() == "" or self.check_password.get() == "confirm password":
            messagebox.showerror("Reset Error", "Please enter and confirm new password.")
            return False
        elif self.reset_password.get() != self.check_password.get():  # 10 characters
            messagebox.showerror("Invalid Password", "New password does not match")
            return False
        else:
            self.username = self.txtusername.get()
            self.password = self.reset_password.get()
            #print(self.username)
            try:
                db.updateuser(self.password, self.username)
                db.refreshdf()
                messagebox.showinfo("", "   Password changed successfuly   ")
                self.loginpage()
            except:
                messagebox.showerror("Password Change Error", "Error saving new password.")
                return False


    def bar(self):

        self.l4=Label(self.window,text='Loading...',fg='white',bg=StartApp.a)
        self.lst5=('Calibri (Body)',9)
        self.l4.config(font=self.lst5)
        self.l4.place(x=18,y=290)
        
        import time
        r=0
        for i in range(100):
            self.progress['value']=r
            self.window.update_idletasks()
            time.sleep(0.03)
            r=r+1
        
        #self.window.destroy()
        self.login_success()


    def login_success(self):
        """after successful login new admin dashboard will open by fetching the current logged in user"""
        user = StartApp.current_user
        userlevel = StartApp.current_user_level
        current_user = user[0]
        current_user_level = userlevel[0]
        SNTree.user.append(current_user)
        SNTree.userlevel.append(current_user_level)
        win = Toplevel()
        SNTree(win)
        self.window.withdraw()
        win.deiconify()

    def onValidate_newpass(self):
        if self.reset_password.get() == self.check_password.get():  # 10 characters
            return True
        else:
            messagebox.showerror("Invalid Password", "New password does not match")
            return False


class Load_Data(Frame):
    user = []
    mydata = []
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.geometry("250x90")
        self.window.title('Load Data')
        self.window.geometry("500x500") # set the root dimensions
        self.window.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
        self.window.resizable(0, 0) # makes the root window fixed in size.
        self.window.iconbitmap(resource_path('lres_icon.ico'))
        #self.top.configure(bg="#2f2f33")
        #self.user = StringVar()

        self.s = ttk.Style()
        self.s.theme_use('default')

        # Frame for TreeView
        self.frame1 = LabelFrame(self.window, text="Excel Data")
        self.frame1.place(height=250, width=500)

        # Frame for open file dialog
        self.file_frame = LabelFrame(self.window, text="Open File")
        self.file_frame.place(height=100, width=400, rely=0.65, relx=0.10)

        # Buttons
        self.button1 = Button(self.file_frame, text="Browse File", width=10, command=lambda: self.file_dialog())
        self.button1.place(rely=0.65, relx=0.10)

        self.button2 = Button(self.file_frame, text="View File", width=10,  command=lambda: self.view_excel_data())
        self.button2.place(rely=0.65, relx=0.40)

        self.button3 = Button(self.file_frame, text="Upload File", width=10, command=lambda: self.upload_excel_data())
        self.button3.place(rely=0.65, relx=0.70)

        # The file/file path text
        self.label_file = Label(self.file_frame, text="No File Selected")
        self.label_file.place(rely=0, relx=0)


        ## Treeview Widget
        self.tv1 = ttk.Treeview(self.frame1)
        self.tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        self.treescrolly = Scrollbar(self.frame1, orient="vertical", command=self.tv1.yview) # command means update the yaxis view of the widget
        self.treescrollx = Scrollbar(self.frame1, orient="horizontal", command=self.tv1.xview) # command means update the xaxis view of the widget
        self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set) # assign the scrollbars to the Treeview Widget
        self.treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        self.treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


    def file_dialog(self):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        self.filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select A File",
                                              filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
        self.label_file["text"] = self.filename
        return None


    def view_excel_data(self):
        """If the file selected is valid this will load the file into the Treeview"""
        if len(self.label_file["text"])<1:
            messagebox.showerror("Select File", "No file selected to view.")
        else:
            self.file_path = self.label_file["text"]
            try:
                self.excel_filename = r"{}".format(self.file_path)
                self.df = pd.read_excel(self.excel_filename, dtype={'IDNo': str, 'HomeNumber': str, 'DOB':str}).fillna("")

            except ValueError:
                messagebox.showerror("Information", "The file you have chosen is invalid")
                return None
            except FileNotFoundError:
                messagebox.showerror("Information", f"No such file as {self.file_path}")
                return None

            Load_Data.mydata.clear()
            self.clear_data()
            
            self.tv1['columns'] = ("RecordNo", "NoDetail", "Claimant", "LastName", "FirstName", "Gender", 
                "IDNo", "DOB", "Deceased", "Eligible", "Dispossessed", 
                "HomeNumber", "PhysicalAddress")
            
            self.tv1["show"] = "headings"
            for column in self.tv1["columns"]:
                self.tv1.heading(column, text=column) # let the column heading = column name

            self.df_rows = self.df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in self.df_rows:
                self.tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
                Load_Data.mydata.append(row)
            return None

    def clear_data(self):
        Load_Data.mydata.clear()
        self.tv1.delete(*self.tv1.get_children())
        return None

    def upload_excel_data(self):
         if len(Load_Data.mydata) < 1:
            messagebox.showerror("Load Error", "No data to load.")
         else:
            self.loadrows = self.df.values.tolist()
            self.duplist=[]
            self.rid_last = db.df_list.values[-1].tolist()[0]
            self.recordnew = self.rid_last + 1
            self.cdate = datetime.datetime.now()
            self.cuser = Load_Data.user[0]
            for i in db.listopt:
                #print("Duplicate ID:" + i[6])
                self.duplist.append(i[6])
            for record in self.loadrows:
                if record[6] in self.duplist and record[6]!="":
                    print("Duplicate ID:" + str(i[6]))
                    pass
                else:
                    db.insertlist(self.recordnew, record[1], record[2], record[3], record[4],
                        record[5], record[6], record[7], record[8], record[9], record[10], record[11], 
                        self.cdate, self.cuser,"", "", "", "", "", "", record[12], "", "", "", "", 0, 0, 0, 
                        "", "", "")
                    self.recordnew +=1
                    #print(record)
                        
            messagebox.showinfo("Data Uploaded", "Your data has been uploaded successfuly.")
            db.refreshdf()
            self.window.destroy()

    def exportcsv(self):
        if len(self.exprows) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        else:
            db.exportlist_csv(self.exprows)
            messagebox.showinfo("Data Exported", "Your data has been exported successfuly.")


    def click_load(self):
        """calls login page when clicked on login button"""
        win = Toplevel()
        SNTree(win)
        self.window.withdraw()
        win.deiconify()




class SNTree(Frame):
    
    a='#249794'
    gen=[]
    user=[]
    userlevel=[]
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.title('LRES BVT')
        #self.window.geometry("1000x670")
        self.window.configure(bg='#141517')
        self.window.resizable(False, False)
        self.window.iconbitmap(resource_path('lres_icon.ico'))

        
        self.window.width_of_window = 1200
        self.window.height_of_window = 650
        self.window.screen_width = self.window.winfo_screenwidth()
        self.window.screen_height = self.window.winfo_screenheight()
        self.window.x_coordinate = (self.window.screen_width/2)-(self.window.width_of_window/2)
        self.window.y_coordinate = (self.window.screen_height/2)-(self.window.height_of_window/2)
        self.window.geometry("%dx%d+%d+%d" %(self.window.width_of_window,self.window.height_of_window,self.window.x_coordinate,self.window.y_coordinate))
        
        #self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
        #center(self.window, width=1200, height=650)
        self.window.protocol("WM_DELETE_WINDOW", self.file_exit)
        

        # Create frame for navigation page
        self.titleframe = Frame(self.window, bg="#2f2f33")
        self.titleframe.pack()
        self.pageframe = Frame(self.window, bg="#2f2f33")
        self.pageframe.pack()
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.clear_tree()


    
    def create_widgets(self):
        #self.img_logo = Image.open("{}".format(sd) + "lres_logo.png")
        self.img_logo = Image.open(resource_path("lres_logo.png"))
        self.resized_logo = self.img_logo.resize((90, 60), Image.ANTIALIAS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)

        ##SETUP MENUBAR##

        #ADD A MENU
        self.my_menu = Menu(self.window)
        self.window.config(menu=self.my_menu, bg="#2f2f33")
        

        #ADD MENU DROPDOWN
        #create file menu item
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Family", command=self.file_open)
        self.file_menu.add_command(label="Add Community")
        self.file_menu.add_command(label="Add Land")
        self.file_menu.add_separator()
        self.file_menu.add_command(labe="Exit", command=self.file_exit)

        #Create a admin menu item
        self.admin_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Admin", menu=self.admin_menu)
        if SNTree.userlevel[0] == 1:
            self.admin_menu.add_command(label="Add Claims", command=self.claim_open)
            self.admin_menu.add_command(label="Export Claims", command=self.exportclaimcsv)

        #Create a help menu item
        self.help_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Documentation", command=self.help_doc)

        #self.filterframe = Frame(self.titleframe, bg="#2f2f33")
        #self.filterframe.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        #self.blklbl6 = Label(self.filterframe, text="" ,  width=14, bg='#2f2f33', font=('Calibri (Body)', 18, 'bold'))
        #self.blklbl6.grid(row=0, column=0, padx=5, pady=5)

        self.typeoptions = [
        "Filter:",
        "Family",
        "Community",
        "Land"
        ]

        #APP OPTION BOX
        #self.typeclicked = StringVar()
        #self.typeclicked.set(self.typeoptions[0])
        #self.typeopt = OptionMenu(self.filterframe, self.typeclicked, *self.typeoptions, command=self.type_status)
        #self.typeopt.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        #self.typeopt.configure(width=11, border=0,fg="#2f2f33",bg='white', activebackground='white', font=('Calibri (Body)', 8))

        #self.blklbl7 = Label(self.filterframe, text="" , bd=1, width=15, bg="#2f2f33")
        #self.blklbl7.grid(row=1, column=1, padx=5, pady=5)

        #self.logolblL = Label(self.filterframe, image=self.new_logo , bg="#2f2f33", foreground="white", font=('Calibri (Body)', 18, 'bold'), anchor=CENTER)
        #self.logolblL.grid(row=0, column=0, padx=5, pady=5)

        #self.blklbl6 = Label(self.filterframe, text="" ,  width=8, bg='#2f2f33', font=('Calibri (Body)', 18, 'bold'))
        #self.blklbl6.grid(row=0, column=1, padx=5, pady=5)

        #self.mainframe = Frame(self.titleframe, bg="#2f2f33")
        #self.mainframe.grid(row=0, column=1, padx=5, pady=5)
        #self.mainframe.pack(padx=20, pady=5)

        self.mainlbl = Label(self.titleframe, text="CAPTURE SYSTEM" , bg="#2f2f33", foreground='white', font=('Calibri (Body)', 18, 'bold'), anchor=CENTER)
        self.mainlbl.grid(row=0, column=0, padx=5, pady=5)

        self.mainframesearch = Frame(self.titleframe, bg="#2f2f33")
        self.mainframesearch.grid(row=1, column=0, padx=5, pady=5)

        #SETUP PRIMARY OPTIONS#
        self.primoptions =[]
        for i in db.claimopt:
            self.primoptions.append(str(i[0])+" - "+i[1]+": "+" ["+str(i[3])+"]")

        #PRIMARY RECORD LABELS
        self.primlbl = Label(self.mainframesearch, text="Search Claim/Project:" , bg="#2f2f33", width=17, foreground="white", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.primlbl.grid(row=0, column=0, padx=5, pady=5)

        #PRIMARY RECORD BOX
        self.primcmb = ttk.Combobox(self.mainframesearch, value=self.primoptions, width=60, font=('Calibri (Body)', 8))
        self.primcmb.grid(row=0, column=1, padx=5, pady=5)
        self.primcmb.bind("<<ComboboxSelected>>", self.get_primary)
        self.primcmb.bind("<KeyRelease>", self.check_input)
        
        #CLEAR BUTTON
        #self.clearbtn = Button(self.wrapper1,  text="x", width=3, command=self.clear_filter, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.clearbtn = Button(self.mainframesearch,  text="Clear Search", width=17, command=self.clear_filter, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.clearbtn.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        #self.blklbl7 = Label(self.mainframesearch, text="" ,  width=39, bg="#2f2f33")
        #self.blklbl7.grid(row=0, column=3, padx=5, pady=5)


        #FAMILY
        #self.fambtn = Button(self.mainframe, text="Add Family", width=17, command=self.fam_entry, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        #self.fambtn.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        #COMMUNITY
        #self.combtn = Button(self.mainframe, text="Add Community", width=17, command=self.com_entry, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        #self.combtn.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        #LAND
        #self.lanbtn = Button(self.mainframe, text="Add Land", width=17, command=self.land_entry, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        #self.lanbtn.grid(row=1, column=2, padx=5, pady=5, sticky=W)

        #self.logoframeR = Frame(self.titleframe, bg="#2f2f33")
        #self.logoframeR.grid(row=0, column=2, padx=5, pady=5)

        #self.logolblR = Label(self.logoframeR, image=self.new_logo , bg="#2f2f33", foreground="white", font=('Calibri (Body)', 18, 'bold'), anchor=CENTER)
        #self.logolblR.grid(row=0, column=0, padx=5, pady=5)

        #SETUP FRAMES
        self.wrapper1 = LabelFrame(self.pageframe, text="Record Search", bg="#2f2f33", foreground="grey", font=('Calibri (Body)', 9, 'bold'))
        #self.wrapper1.pack(fill="both", padx=20, pady=10)
        self.wrapper1.grid(row=1, column=0, padx=5, pady=5)


        self.appoptions = [
        "Finalisation",
        "Phased",
        "Settlement",
        "Negotiatons",
        "Valuation",
        "Options",
        "Verification", 
        "Research",
        "Non-compliant"
        ]

        self.compoptions = [
        "Complete",
        "Incomplete"
        ]

        self.odioptions = []

        self.odispoptions = []

        self.desoptions = []

        self.desidoptions = []

        self.comoptions = []

        self.memoptions = []

        self.propoptions = []

        self.landoptions = []

        self.optionssp = []

        self.options3 = []

        self.options4 = []

        self.options5 = []

        self.options6 = []

        self.options7 = []

        self.ridoptions = []

        self.rloptions = {
        "First Generation":3,
        "Second Generation":4,
        "Third Generation":5,
        "Fourth Generation":6, 
        "Fifth Generation":7
        }

        self.genoptions = {
        "ODI":1,
        "ODI Spouse/Partner":2,
        "First Generation":3,
        "Second Generation":4, 
        "Third Generation":5, 
        "Fourth Generation":6, 
        "Fifth Generation":7
        }

        self.genrloptions = {
        1:{"":["ODI", "Estate Executor"]},
        2:{"":["ODI Spouse", "Customary Spouse", "Life Partner", "Household Partner", "Estate Executor"]},
        3:{"First Generation":["Child", "Estate Executor"]},
        4:{"Second Generation":["Grandchild", "Estate Executor"]}, 
        5:{"Third Generation":["Great Grandchild", "Estate Executor"]}, 
        6:{"Fourth Generation":["Great Great Grandchild", "Estate Executor"]}, 
        7:{"Fifth Generation":["Great Great Great Grandchild", "Estate Executor"]},
        8:{"":[""]}
        }


        self.useroptions=[]
        self.useroptions.append("Filter:")
        for i in db.useropt:
            self.useroptions.append(i[1])
    

        #BLANK RECORD LABELS
        #self.blklbl1 = Label(self.wrapper1, text="" , width=44, bg="#2f2f33",  font=('Calibri (Body)', 8))
        #self.blklbl1.grid(row=1, column=2, padx=5, pady=5)


        #SEARCH FAMILY CLAIMS
        self.fam = ToggledFrame(self.wrapper1, text='Family', relief="raised", borderwidth=1)
        self.fam.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        #LINK RECORD LABELS
        self.linklbl = Label(self.fam.sub_frame, text="Select ODI:" , width=17, bg="light grey",  foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        #self.linklbl.pack(side="left", pady=2, padx=5)
        self.linklbl.grid(row=1, column=0, padx=2, pady=2, sticky=W)

        #LINK COMBO BOX
        self.linkcmb = ttk.Combobox(self.fam.sub_frame, value=self.odioptions, width=36, font=('Calibri (Body)', 8))
        #self.linkcmb.pack(side="left", pady=2, padx=5)
        self.linkcmb.grid(row=2, column=0, padx=2, pady=2, sticky=W)
        self.linkcmb.bind("<<ComboboxSelected>>", self.get_odi)

        #LINK RECORD LABELS
        self.link3lbl = Label(self.fam.sub_frame, text="Select ODI Spouse:" , width=17, bg="light grey", foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        #self.link3lbl.pack(side="left", pady=2, padx=5)
        self.link3lbl.grid(row=3, column=0, padx=2, pady=2, sticky=W)

        #LINK COMBO BOX
        self.link3cmb = ttk.Combobox(self.fam.sub_frame, value=self.odispoptions, width=36, font=('Calibri (Body)', 8))
        self.link3cmb.grid(row=4, column=0, padx=2, pady=2, sticky=W)
        #self.link3cmb.pack(side="left", pady=2, padx=5)
        self.link3cmb.bind("<<ComboboxSelected>>", self.get_odispouse)

        #RELATIONSHIP LABEL
        self.rllbl = Label(self.fam.sub_frame, text="Select Generation:" , width=17, bg="light grey",  foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.rllbl.grid(row=5, column=0, padx=2, pady=2, sticky=W)
        #self.rllbl.pack(side="left", pady=2, padx=5)

        #RELATIONSHIP COMBO
        self.rlopt = StringVar()
        self.rlcmb = ttk.Combobox(self.fam.sub_frame, value=list(self.rloptions.keys()), width=36, textvariable=self.rlopt, font=('Calibri (Body)', 8))
        self.rlcmb.set('')
        self.rlcmb.grid(row=6, column=0, padx=2, pady=2, sticky=W)
        #self.rlcmb.pack(side="left", pady=2, padx=5)
        self.rlcmb.bind("<<ComboboxSelected>>", self.get_rlkey)

        #LINK RECORD LABELS
        self.link2lbl = Label(self.fam.sub_frame, text="Select Descendants:" , width=17, bg="light grey",  foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.link2lbl.grid(row=7, column=0, padx=2, pady=2, sticky=W)
        #self.link2lbl.pack(side="left", pady=2, padx=2)

        #LINK COMBO BOX
        self.link2cmb = ttk.Combobox(self.fam.sub_frame, value=self.desoptions, width=36, font=('Calibri (Body)', 8))
        self.link2cmb.grid(row=8, column=0, padx=2, pady=(2,5), sticky=W)
        #self.link2cmb.pack(side="left", pady=2, padx=2)
        self.link2cmb.bind("<<ComboboxSelected>>", self.get_desc)

        #SEARCH COMMUNITY CLAIMS
        self.com = ToggledFrame(self.wrapper1, text='Community', relief="raised", borderwidth=1)
        self.com.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        #LINK RECORD LABELS
        self.linklblcom = Label(self.com.sub_frame, text="Select Community:" , width=17, bg="light grey", foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.linklblcom.grid(row=9, column=0, padx=2, pady=2, sticky=W)
        #self.linklblcom.pack(side="left", pady=2, padx=5)

        #LINK COMBO BOX
        self.linkcmbcom = ttk.Combobox(self.com.sub_frame, value=self.comoptions, width=36, font=('Calibri (Body)', 8))
        self.linkcmbcom.grid(row=10, column=0, padx=2, pady=2)
        #self.linkcmbcom.pack(side="left", pady=2, padx=5)
        self.linkcmbcom.bind("<<ComboboxSelected>>", self.get_com)

        #LINK RECORD LABELS
        self.linklblmem = Label(self.com.sub_frame, text="Select Member:" , width=17, bg="light grey",  foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.linklblmem.grid(row=11, column=0, padx=2, pady=2, sticky=W)
        #self.linklblmem.pack(side="left", pady=2, padx=2)

        #LINK COMBO BOX
        self.linkcmbmem = ttk.Combobox(self.com.sub_frame, value=self.memoptions, width=36, font=('Calibri (Body)', 8))
        self.linkcmbmem.grid(row=12, column=0, padx=2, pady=(2,5), sticky=W)
        #self.linkcmbmem.pack(side="left", pady=2, padx=2)
        self.linkcmbmem.bind("<<ComboboxSelected>>", self.get_mem)

        #SEARCH LAND CLAIMS
        self.land = ToggledFrame(self.wrapper1, text='Land', relief="raised", borderwidth=1)
        self.land.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        #LINK RECORD LABELS
        self.linklblprop = Label(self.land.sub_frame, text="Select Property:" , width=17, bg="light grey",  foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.linklblprop.grid(row=13, column=0, padx=2, pady=2, sticky=W)
        #self.linklblprop.pack(side="left", pady=2, padx=2)

        #LINK COMBO BOX
        self.linkcmbprop = ttk.Combobox(self.land.sub_frame, value=self.propoptions, width=36, font=('Calibri (Body)', 8))
        self.linkcmbprop.grid(row=14, column=0, padx=2, pady=2, sticky=W)
        #self.linkcmbprop.pack(side="left", pady=2, padx=5)
        self.linkcmbprop.bind("<<ComboboxSelected>>", self.get_prop)

        #LINK RECORD LABELS
        self.linklblland = Label(self.land.sub_frame, text="Select Parcel:" , width=17, bg="light grey",  foreground="black", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.linklblland.grid(row=15, column=0, padx=2, pady=2, sticky=W)
        #self.linklblland.pack(side="left", pady=2, padx=2)

        #LINK COMBO BOX
        self.linkcmbland = ttk.Combobox(self.land.sub_frame, value=self.landoptions, width=36, font=('Calibri (Body)', 8))
        self.linkcmbland.grid(row=16, column=0, padx=2, pady=(2,5), sticky=W)
        #self.linkcmbland.pack(side="left", pady=2, padx=2)
        self.linkcmbland.bind("<<ComboboxSelected>>", self.get_prop)

        #self.blklbl2 = Label(self.wrapper1, text="" , width=17, bg="#2f2f33")
        #self.blklbl3 = Label(self.wrapper1, text="" , width=17, bg="#2f2f33")
        #self.blklbl4 = Label(self.wrapper1, text="" , width=17, bg="#2f2f33")

        #self.blklbl2.grid(row=11, column=0, padx=5, pady=5)
        #self.blklbl3.grid(row=12, column=0, padx=5, pady=5)
        #self.blklbl4.grid(row=13, column=0, padx=5, pady=5)

        #SETUP NOTEBOOK
        self.create_notebook()

        #END FRAME
        self.right_frame = Frame(self.window, bg="#2f2f33")
        self.right_frame.pack(padx=20, pady=5, side=RIGHT)

        self.left_frame = Frame(self.window, bg="#2f2f33")
        self.left_frame.pack(padx=20, side=LEFT)

        #EXIT BUTTON
        self.exitbtn = Button(self.right_frame, text="Exit", width=17, command=self.file_exit, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.exitbtn.grid(row=0, column=1,  padx=5, pady=5)

        #CURRENT USER
        self.userlogin = StringVar()
        self.current_user = Label(self.left_frame, text=f"Signed in: {SNTree.user[0]}", bg="#2f2f33", font=('Calibri (Body)', 6),fg=SNTree.a)
        #self.current_user = Label(self.left_frame, text=f"Signed in: ", bg="white", font=('Calibri (Body)', 6),fg=SNTree.a)
        self.current_user.grid(row=0, column=0,  padx=5, pady=5)
        self.euser = Entry(self.left_frame, textvariable=self.userlogin, width=10, bd=0, bg="#2f2f33", fg="#2f2f33", font=('Calibri (Body)', 6))
        self.euser.grid(row=0, column=1, padx=5)
        self.euser.insert(0, SNTree.user[0])
        #self.euser.insert(0, "")

        '''
        if SNTree.user[0] == "Patricia Chirwa":
            self.my_menu.config
        '''



    def create_notebook(self):
        #SETUP FRAME
        self.wrapper2 = LabelFrame(self.pageframe, text="Record Link", bg="#2f2f33", foreground="grey", font=('Calibri (Body)', 9, 'bold'))
        #self.wrapper2.pack(fill="both", padx=20, pady=(10,5))
        self.wrapper2.grid(row=1, column=1, padx=5, pady=5)

        #CREATE NOTEBOOK TABS
        self.my_notebook = ttk.Notebook(self.wrapper2)
        self.my_notebook.pack(fill="both", expand=1)

        self.list_frame = Frame(self.my_notebook, bg="light grey")
        self.fam_frame = Frame(self.my_notebook, bg="light grey")
        self.com_frame = Frame(self.my_notebook, bg="light grey")
        self.lan_frame = Frame(self.my_notebook, bg="light grey")
    
        self.list_frame.pack(fill="both", expand=1)
        self.fam_frame.pack(fill="both", expand=1)
        self.com_frame.pack(fill="both", expand=1)
        self.lan_frame.pack(fill="both", expand=1)

        self.my_notebook.add(self.list_frame, text="Claim Records")
        self.my_notebook.add(self.fam_frame, text="Family Records")
        self.my_notebook.add(self.com_frame, text="Community Records")
        self.my_notebook.add(self.lan_frame, text="Land Records")


        self.my_notebook_fam = ttk.Notebook(self.fam_frame)
        self.my_notebook_fam.pack(fill="both", expand=1)
        self.link_frame_fam = Frame(self.my_notebook_fam, bg="light grey")
        self.new_frame_fam = Frame(self.my_notebook_fam, bg="light grey")

        self.new_frame_fam.pack(fill="both", expand=1)
        self.link_frame_fam.pack(fill="both", expand=1)

        self.my_notebook_fam.add(self.new_frame_fam, text="New Records")
        self.my_notebook_fam.add(self.link_frame_fam, text="Linked Records")


        self.my_notebook_com = ttk.Notebook(self.com_frame)
        self.my_notebook_com.pack(fill="both", expand=1)
        self.link_frame_com = Frame(self.my_notebook_com, bg="light grey")
        self.new_frame_com = Frame(self.my_notebook_com, bg="light grey")

        self.new_frame_com.pack(fill="both", expand=1)
        self.link_frame_com.pack(fill="both", expand=1)

        self.my_notebook_com.add(self.new_frame_com, text="New Records")
        self.my_notebook_com.add(self.link_frame_com, text="Linked Records")


        self.my_notebook_lan = ttk.Notebook(self.lan_frame)
        self.my_notebook_lan.pack(fill="both", expand=1)
        self.link_frame_lan = Frame(self.my_notebook_lan, bg="light grey")
        self.new_frame_lan = Frame(self.my_notebook_lan, bg="light grey")

        self.new_frame_lan.pack(fill="both", expand=1)
        self.link_frame_lan.pack(fill="both", expand=1)

        self.my_notebook_lan.add(self.new_frame_lan, text="New Records")
        self.my_notebook_lan.add(self.link_frame_lan, text="Linked Records")



        #def setup_treeview(self, frame, height):
        #LOAD IMAGES
        '''
        self.img_arrow = ImageTk.PhotoImage(Image.open("{}".format(sd) + "arrow.png"))
        self.img_comp = ImageTk.PhotoImage(Image.open("{}".format(sd) + "complete.png"))
        self.img_child = ImageTk.PhotoImage(Image.open("{}".format(sd) + "child.png"))
        self.img_nochild = ImageTk.PhotoImage(Image.open("{}".format(sd) + "nochild.png"))
        '''
        self.img_arrow = ImageTk.PhotoImage(Image.open(resource_path("arrow.png")))
        self.img_comp = ImageTk.PhotoImage(Image.open(resource_path("complete.png")))
        self.img_child = ImageTk.PhotoImage(Image.open(resource_path("child.png")))
        self.img_nochild = ImageTk.PhotoImage(Image.open(resource_path("nochild.png")))

        self.img_refresh = Image.open("{}".format(sd) + "refresh2.png")
        self.img_refresh = Image.open(resource_path("refresh2.png"))
        self.resized = self.img_refresh.resize((18,16), Image.ANTIALIAS)
        self.new_refresh = ImageTk.PhotoImage(self.resized)
        

        #SETUP TREEVIEW

        self.tree_frame=Frame(self.list_frame, bg="light grey")
        #self.status_frame.pack(side= LEFT)
        self.tree_frame.grid(row=0, padx=5, pady=5, sticky=W)

        self.my_tree = ttk.Treeview(self.tree_frame, height="16")
        self.my_tree.pack(side= LEFT)
        #self.my_tree.grid(row=0, padx=5, pady=5, sticky=W)

        self.status_frame=Frame(self.list_frame, bg="light grey")
        #self.status_frame.pack(side= LEFT)
        self.status_frame.grid(row=1, padx=5, pady=5, sticky=W)

        #self.my_treestat = label(self.list_frame, )

        self.style = ttk.Style(self.my_tree)
        self.style.theme_use("default")
        #configure treeview style

        self.style.layout("Treeview.Item", [
        ('Treeitem.padding', {'sticky': 'nswe','children': [
        ('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
        ('Treeitem.image', {'side': 'left', 'sticky': ''}),
        ('Treeitem.text', {'side': 'left', 'sticky': ''}),
        ],
        })]
        )

        self.style.configure("Treeview",
            bd=0,
            background="white",
            foreground="black",
            rowheight = 23,
            fieldbackground="silver",
            font=('Calibri (Body)', 9))
        self.style.map('Treeview',
            background=[('selected', SNTree.a)],
            foreground=[('selected', 'black')])

        self.style.configure("Treeview.Heading",
            font=('Calibri (Body)', 9))


        #ADD SCROLLBAR
        self.tree_scroll = Scrollbar(self.tree_frame, orient="vertical", command=self.my_tree.yview)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        #CONFIGURE SCROLLBAR
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)

        #DEFINE COLUMNS
        self.my_tree['columns'] = ("ClaimantReference", "Generation", "BenID", "LinkID", "Name", "Relationship")

        #FORMAT COLUMNS
        self.my_tree.column("#0", width=118, stretch=0, anchor=W)
        self.my_tree.column("ClaimantReference", anchor=W, width=138)
        self.my_tree.column("Generation", anchor=W, width=120)
        self.my_tree.column("BenID", anchor=W, width=58)
        self.my_tree.column("LinkID", anchor=W, width=58)
        self.my_tree.column("Name", anchor=W, width=240)
        self.my_tree.column("Relationship", anchor=W, width=125)

        #CREATE HEADINGS
        self.my_tree.heading("#0", text="Link", anchor=W)
        self.my_tree.heading("ClaimantReference", text="Claim Reference", anchor=W)
        self.my_tree.heading("Generation", text="Generation", anchor=W)
        self.my_tree.heading("BenID", text="Record ID", anchor=W)
        self.my_tree.heading("LinkID", text="Link ID", anchor=W)
        self.my_tree.heading("Name", text="Name", anchor=W)
        self.my_tree.heading("Relationship", text="Relationship", anchor=W)


        #SETUP TAGS
        self.my_tree.tag_configure('arrow', image=self.img_arrow)
        self.my_tree.tag_configure('primcomplete', image=self.img_arrow)
        self.my_tree.tag_configure('primary', image=self.img_nochild)
        self.my_tree.tag_configure('child', image=self.img_child)
        self.my_tree.tag_configure('childdeceased', foreground="grey", image=self.img_child)

        #APP OPTION BOX
        self.appclicked = StringVar()
        self.appclicked.set(self.appoptions[7])
        self.appopt = OptionMenu(self.status_frame, self.appclicked, *self.appoptions, command=self.app_status)
        self.appopt.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.appopt.configure(width=11, border=0,fg="#2f2f33",bg='white', activebackground='white', font=('Calibri (Body)', 8))

        #COMPLETE OPTION BOX
        self.compclicked = StringVar()
        self.compclicked.set(self.compoptions[1])
        self.compopt = OptionMenu(self.status_frame, self.compclicked, *self.compoptions, command=self.complete_status)
        self.compopt.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.compopt.configure(width=11, border=0,fg="#2f2f33",bg='white', activebackground='white', font=('Calibri (Body)', 8))

        #BLANK RECORD LABELS
        self.blklbl5 = Label(self.status_frame, text="" , width=86, bg="light grey",  font=('Calibri (Body)', 8))
        self.blklbl5.grid(row=0, column=2, padx=5, pady=5)

        #DELETE BUTTON
        self.delbtn = Button(self.status_frame, text="Delete Link", width=16, command=self.delete_link, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.delbtn.grid(row=0, column=3, padx=5, pady=5, sticky=E)

        #def setup_listview(self, frame, height, mid, mtype, pid, fn, ln, idno):
        
        #CREATE NEW DATA PAGE
        self.newgen_frame=Frame(self.new_frame_fam, width=120, bg="light grey")
        self.newgen_frame.grid(row=0, padx=5, pady=5, sticky=W)

        self.newparentlbl = Label(self.newgen_frame, text="Linked Parent Record:", width=15, bg="light grey", foreground="black", font=('Calibri (Body)', 7, "bold"), anchor=W)
        self.newparentlbl.grid(row=0, column=0, padx=5, pady=5)
        
        #create an entry box
        self.parentnewbx = Entry(self.newgen_frame, font=('Calibri (Body)', 8), width=47)
        self.parentnewbx.grid(row=0, column=1, padx=5, pady=5)


        #CLEAR BUTTON
        #self.clearnewbtn = Button(self.newsearch_frame, text="x", width=3, command=self.refresh_lst, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.clearnewbtn = Button(self.newgen_frame,  image=self.new_refresh, command=self.refresh_lst, border=0,fg='black',bg='grey', activebackground='white', font=('Calibri (Body)', 8))
        self.clearnewbtn.grid(row=0, column=3, padx=5, pady=5, sticky=E)

        self.newgenrllbl = Label(self.newgen_frame, text="Select Relationship:", width=15, bg="light grey", foreground="black", font=('Calibri (Body)', 7, "bold"), anchor=W)
        self.newgenrllbl.grid(row=1, column=0, padx=5, pady=5)

        self.newgenopt2 = StringVar()
        #self.newgencmb2 = ttk.Combobox(self.newgen_frame, value=list(self.genrloptions.keys()), width=44, textvariable=self.newgenopt2, font=('Calibri (Body)', 8))
        self.newgencmb2 = ttk.Combobox(self.newgen_frame, width=45, textvariable=self.newgenopt2, font=('Calibri (Body)', 8))
        self.newgencmb2.grid(row=1, column=1, padx=5, pady=5)
        self.newgencmb2.set('')
        self.newgencmb2.bind("<<ComboboxSelected>>", self.rl_newbx)

        #BLANK RECORD LABELS
        self.blklbl1 = Label(self.newgen_frame, text="" , width=48, bg="light grey",  font=('Calibri (Body)', 8))
        self.blklbl1.grid(row=1, column=2, padx=5, pady=5)

        self.userclicked1 = StringVar()
        self.userclicked1.set(self.useroptions[0])
        self.useopt1 = OptionMenu(self.newgen_frame, self.userclicked1, *self.useroptions, command=self.user_status)
        self.useopt1.grid(row=1, column=3, padx=5, pady=5, sticky=E)
        self.useopt1.configure(width=17, border=0,fg="#2f2f33",bg='white', activebackground='white', font=('Calibri (Body)', 8))

        #setup frame and scrollbar
        self.newlst_frame=Frame(self.new_frame_fam)
        self.newlst_frame.grid(row=1, padx=5, pady=5, sticky=W)
        self.newlst_scroll = Scrollbar(self.newlst_frame, orient="vertical")

        #create a listbox
        self.searchnewlst = Listbox(self.newlst_frame, width=122, font=('Calibri (Body)', 9), height="17", selectbackground=SNTree.a, selectmode=EXTENDED, yscrollcommand=self.newlst_scroll.set)
        self.newlst_scroll.config(command=self.searchnewlst.yview)
        self.newlst_scroll.pack(side=RIGHT, fill=Y)
        self.searchnewlst.pack(pady=5)

        #bind listbox
        self.searchnewlst.bind("<<ListboxSelect>>", self.fill_newlst)

        self.newsearch_frame=Frame(self.new_frame_fam, bg="light grey")
        self.newsearch_frame.grid(row=2, padx=5, pady=5, sticky=W)
        self.searchnewlbl = Label(self.newsearch_frame, text="Link New Record:", width=15, bg="light grey", foreground="black", font=('Calibri (Body)', 7, "bold"), anchor=W)
        self.searchnewlbl.grid(row=0, column=0, padx=5, pady=5)
        
        #create an entry box
        self.searchnewbx = Entry(self.newsearch_frame, font=('Calibri (Body)', 8), width=47)
        self.searchnewbx.grid(row=0, column=1, padx=5, pady=5)
        self.searchnewbx.bind("<KeyRelease>", self.check_newlst)

        #BLANK RECORD LABELS
        #self.blklbl1 = Label(self.newsearch_frame, text="" , width=12, bg="light grey",  font=('Calibri (Body)', 8))
        #self.blklbl1.grid(row=0, column=2, padx=5, pady=5)

        #self.newend_frame=Frame(self.new_frame_fam, bg="light grey")
        #self.newend_frame.grid(row=3, padx=5, pady=5, sticky=W)

        #LINK BUTTON
        self.linknewbtn = Button(self.newsearch_frame, text="Link Record", width=16, command=self.new_record, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.linknewbtn.grid(row=0, column=3, padx=5, sticky=W)

        self.searchnewbx["state"]=DISABLED
        self.linknewbtn["state"] = DISABLED

        self.newrec = []
        self.lastcol = len(db.df_newlist.columns)-1
        for i in db.newlistopt:
            if i[self.lastcol] == "left_only":
                self.newrec.append(str(i[0])+" - "+i[4]+" "+i[3] +": ["+str(i[6])+"]")

        self.update_newlst(self.newrec)

        #DELETE BUTTON
        self.delnewbtn = Button(self.newsearch_frame, text="Delete Record", width=16, command=self.delete_newlist, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.delnewbtn.grid(row=0, column=4, padx=5, sticky=E)

        #ADD Button
        self.addbtn_fam = Button(self.newsearch_frame, text="Add Record", width=17, command=self.fam_entry, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.addbtn_fam.grid(row=0, column=5, padx=5, pady=5, sticky=W)

        #LOAD BUTTON
        self.loadbtn_fam = Button(self.newsearch_frame, text="Load Record", width=17, command=self.fam_open, border=0, fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.loadbtn_fam.grid(row=0, column=6, padx=5, sticky=E)


        #CREATE LINK DATA PAGE
        #create label
        self.linkgen_frame=Frame(self.link_frame_fam, bg="light grey")
        self.linkgen_frame.grid(row=0, padx=5, pady=5, sticky=W)

        self.linkparentlbl = Label(self.linkgen_frame, text="Linked Parent Record:", width=15, bg="light grey", foreground="black", font=('Calibri (Body)', 7, "bold"), anchor=W)
        self.linkparentlbl.grid(row=0, column=0, padx=5, pady=5)
        
        #create an entry box
        self.parentlinkbx = Entry(self.linkgen_frame, font=('Calibri (Body)', 8), width=47)
        self.parentlinkbx.grid(row=0, column=1, padx=5, pady=5)
        self.parentlinkbx.bind('<Return>', self.check_parentlst)

        #BLANK RECORD LABELS
        #self.parentlinkbtn = Button(self.linkgen_frame, text="Search" , width=16, command=self.check_linklst_btn, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        #self.parentlinkbtn.grid(row=0, column=2, padx=5, pady=5, sticky=W)


        #CLEAR BUTTON
        #self.clearlinkbtn = Button(self.linksearch_frame,  text="x", width=3, command=self.refresh_lst, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.clearlinkbtn = Button(self.linkgen_frame,  image=self.new_refresh, command=self.refresh_lst, border=0,fg='black',bg='grey', activebackground='white', font=('Calibri (Body)', 8))
        self.clearlinkbtn.grid(row=0, column=3, padx=5, pady=5, sticky=E)

        self.linkgenrllbl = Label(self.linkgen_frame, text="Select Relationship:", width=15, bg="light grey", foreground="black", font=('Calibri (Body)', 7, "bold"), anchor=W)
        self.linkgenrllbl.grid(row=1, column=0, padx=5, pady=5)

        self.linkgenopt2 = StringVar()
        #self.linkgencmb2 = ttk.Combobox(self.linkgen_frame, value=list(self.genrloptions), width=44, textvariable=self.linkgenopt2, font=('Calibri (Body)', 8))
        self.linkgencmb2 = ttk.Combobox(self.linkgen_frame, width=45, textvariable=self.linkgenopt2, font=('Calibri (Body)', 8))
        self.linkgencmb2.grid(row=1, column=1, padx=5, pady=5)
        self.linkgencmb2.set('')
        self.linkgencmb2.bind("<<ComboboxSelected>>", self.rl_linkbx)

        #BLANK RECORD LABELS
        self.blklbl1 = Label(self.linkgen_frame, text="" , width=48, bg="light grey",  font=('Calibri (Body)', 8))
        self.blklbl1.grid(row=1, column=2, padx=5, pady=5)

        self.userclicked2 = StringVar()
        self.userclicked2.set(self.useroptions[0])
        self.useopt2 = OptionMenu(self.linkgen_frame, self.userclicked2, *self.useroptions, command=self.user_status)
        self.useopt2.grid(row=1, column=3, padx=5, pady=5, sticky=E)
        self.useopt2.configure(width=17, border=0,fg="#2f2f33",bg='white', activebackground='white', font=('Calibri (Body)', 8))


        #Setup frame and scrollbar
        self.linklst_frame=Frame(self.link_frame_fam)
        self.linklst_frame.grid(row=1, padx=5, pady=5, sticky=W)
        self.linklst_scroll = Scrollbar(self.linklst_frame, orient="vertical")

        #create a listbox
        self.searchlinklst = Listbox(self.linklst_frame, width=122, font=('Calibri (Body)', 9), height="17", selectbackground=SNTree.a, selectmode=EXTENDED, yscrollcommand=self.linklst_scroll.set)
        self.linklst_scroll.config(command=self.searchlinklst.yview)
        self.linklst_scroll.pack(side=RIGHT, fill=Y)
        self.searchlinklst.pack(pady=5)

        #bind listbox'
        self.searchlinklst.bind("<<ListboxSelect>>", self.fill_linklst)

        self.linksearch_frame=Frame(self.link_frame_fam, bg="light grey")
        self.linksearch_frame.grid(row=2, padx=5, pady=5, sticky=W)
        self.searchlinklbl = Label(self.linksearch_frame, text="Link Linked Record:", width=15, bg="light grey", foreground="black", font=('Calibri (Body)', 7, "bold"), anchor=W)
        self.searchlinklbl.grid(row=0, column=0, padx=5, pady=5)
        
        #create an entry box
        self.searchlinkbx = Entry(self.linksearch_frame, font=('Calibri (Body)', 8), width=47)
        self.searchlinkbx.grid(row=0, column=1, padx=5, pady=5)
        #bind entry box
        self.searchlinkbx.bind("<KeyRelease>", self.check_linklst)

        #BLANK RECORD LABELS
        self.blklbl4 = Label(self.linksearch_frame, text="" , width=18, bg="light grey",  font=('Calibri (Body)', 8))
        self.blklbl4.grid(row=0, column=2, padx=5, pady=5)

        #self.linkend_frame=Frame(self.link_frame_fam, bg="light grey")
        #self.linkend_frame.grid(row=3, padx=5, pady=5, sticky=W)

        #LINK BUTTON
        self.linkbtn = Button(self.linksearch_frame, text="Link Record", width=16, command=self.link_record, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.linkbtn.grid(row=0, column=3, padx=5, sticky=E)

        self.searchlinkbx["state"]=DISABLED
        self.linkbtn["state"] = DISABLED


        #upload listbox options
        self.linkrec = []
        for i in db.linklistopt:
            self.linkrec.append(str(i[2])+" - "+i[15]+" "+i[14]+": ["+str(i[17])+"]")

        self.update_linklst(self.linkrec)

        #DELETE BUTTON
        self.dellinkbtn = Button(self.linksearch_frame, text="Delete Link", width=16, command=self.delete_linklist, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.dellinkbtn.grid(row=0, column=4, padx=5, sticky=E)

        #LOOKUP BUTTON
        self.editbtn_fam = Button(self.linksearch_frame, text="Edit Record", width=16, command=self.view_record, border=0,fg='black',bg='white', activebackground='white', font=('Calibri (Body)', 8))
        self.editbtn_fam.grid(row=0, column=5, padx=5, pady=5, sticky=E)


    #DEFINE FILE OPEN FUNCTION
    def file_open(self):
        #if messagebox.askyesno("Confirm New File Open?", "Are you sure you want to open a new file?" +"\n"+ "Warning: All unsaved changes to this current file will be lost"):
        win = Toplevel()
        Load_Data(win)
        Load_Data.user.append(self.userlogin.get())

    def fam_open(self):
        #if messagebox.askyesno("Confirm New File Open?", "Are you sure you want to open a new file?" +"\n"+ "Warning: All unsaved changes to this current file will be lost"):
        win = Toplevel()
        Load_Data(win)
        Load_Data.user.append(self.userlogin.get())

    def com_open(self):
        #if messagebox.askyesno("Confirm New File Open?", "Are you sure you want to open a new file?" +"\n"+ "Warning: All unsaved changes to this current file will be lost"):
        win = Toplevel()
        Load_Data(win)
        Load_Data.user.append(self.userlogin.get())

    def land_open(self):
        #if messagebox.askyesno("Confirm New File Open?", "Are you sure you want to open a new file?" +"\n"+ "Warning: All unsaved changes to this current file will be lost"):
        win = Toplevel()
        Load_Data(win)
        Load_Data.user.append(self.userlogin.get())

    #DEFINE CLAIM OPEN FUNCTION
    def claim_open(self):
        #if messagebox.askyesno("Confirm New File Open?", "Are you sure you want to open a new file?" +"\n"+ "Warning: All unsaved changes to this current file will be lost"):
        win = Toplevel()
        Claim_Data(win)
        Claim_Data.user.append(self.userlogin.get())

    #DEFINE QUIT FUNCTION
    def file_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.quit()

    #DEFINE SAVE FUNCTION
    def file_save(self):
        db.filesave()
        messagebox.showinfo("Data Saved", "Your data has been saved successfuly.")
        

    #DEFINE EXPORT FUNCTION
    def file_export(self):
        #filename = filedialog.asksaveasfilename(initialdir=os.getcwd, title="Save File", filetypes=)
        self.filename = filedialog.asksaveasfilename(
            initialdir="C:/Users/User/Dropbox/Python/LRNetworks",
            title = "Save File",
            filetype = (("xlsx Files", "*.xlsx"), ("xls Files", "*.xls"), ("All Files", "*.*"))
            )

        db.filesave(self.filename)
        messagebox.showinfo("Data Exported", "Your data has been exported successfuly.")

    def exportlinkcsv(self):
        cur.execute("SELECT * FROM tblClaimFamLink")
        self.exprows_link = db.fetchlink

        if len(self.exprows_link) < 1:
            messagebox.showerror("No Data", "No data available to save")
            return False
        else:
            db.exportlink_csv(self.exprows_link)
            #messagebox.showinfo("Data Exported", "Your data has been exported successfuly.")

    def exportclaimcsv(self):
        self.exprows_claim = db.fetchclaim

        if len(self.exprows_claim) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        else:
            db.exportclaim_csv(self.exprows_claim)
            messagebox.showinfo("Data Exported", "Your data has been exported successfuly.")


    def exportusercsv(self):
        self.exprows_user = db.fetchuser

        if len(self.exprows_user) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        else:
            db.exportuser_csv(self.exprows_user)
            messagebox.showinfo("Data Exported", "Your data has been exported successfuly.")


    #DEFINE HELP FUNCTION
    def help_doc(self):
        pass

        
    #DEFINE UPLOAD FUNCTION
    def upload(self, linkrows):
        self.my_tree.delete(*self.my_tree.get_children())

        for record in linkrows: 
            #if record[2] == "Finalisation":
            self.my_tree.insert(parent='', index='end', iid=record[0], text= (""), values=(record[6], "", record[0], "", record[1] , ""), tags=('primary',))

            #self.my_tree.insert(parent='', index='end', iid=record[0], text= (""), values=(record[6], "", record[0], "", record[1] , "", record[11]), tags=('primary',))

    #DEFINE CHILDREN FUNCTION
    def upload_child(self, linkchildrows):
        
        self.remainder = []
        self.record_list = []
        self.record_link = []

        for record in linkchildrows:
            self.record_list.append(str(record[0]))
            self.record_link.append(str(record[1]))
            try:
                if record[12] == True:
                    self.my_tree.insert(parent=record[7], index='end', iid=record[6], text= (""), values=("", record[10], record[0], record[1], record[2] +" "+ record[3] + ' (D)', record[4]), tags=('primary',))
                    self.my_tree.item(record[7], tags=('child',))

                else: 
                    self.my_tree.insert(parent=record[7], index='end', iid=record[6], text= (""), values=("", record[10], record[0], record[1], record[2] +" "+ record[3], record[4]), tags=('primary',))
                    self.my_tree.item(record[7], tags='child')
            
            except Exception:
                #print(record[0])
                self.remainder.append(record) 
                pass

        #print(remainder) 
        '''
        self.odi_el = []
        self.odi_award = StringVar
        self.odi_dec = []
        for record in linkchildrows:  
            if record[11] = 1:      
                if record[13] = True:
                    self.odi_el.append(record[6])
                    print(self.odi_el)

                if record[13] = True:
                    self.odi_award = record[14]/len(odi_el)
                    db.updateaward(self.odi_award, record[6])

                
        

                #DEFINE COMPLETE STATUS FUNCTION
    def complete_status(self, event):
        self.primary = self.primcmb.get()
        if len(self.primary) < 1:
            return False
        else:
            self.primaryid = int(self.primary.split(" - ")[0])
            #print(self.compclicked.get())
            self.comp = self.compclicked.get()
            db.updateprogress(self.comp, self.primaryid)
            self.filter_claim(self.primaryid)

            if record[11] = 2: 
                self.mytree.parent(record[7])
                if record[12] == True and record[13] = True:





        '''

    #DEFINE CLEAR FUNCTION
    def clear_tree(self):
        self.linkrows = db.fetchclaim()
        self.upload(self.linkrows)
        self.linkchildrows = db.fetchlistlink()
        self.upload_child(self.linkchildrows)


    #DEFINE FILTER FUNCTION
    def filter_claim(self, prime):
        self.linkrows = db.filterclaim(int(prime))
        self.upload(self.linkrows)
        self.linkchildrows = db.filterlink(int(prime))
        self.upload_child(self.linkchildrows)


    #DEFINE CLEAR FILTER FUNCTION
    def clear_filter(self):
        #clear entry boxes
        self.primcmb.set("")
        self.linkcmb.set('')
        self.link3cmb.set('')
        self.rlcmb.set('')
        self.link2cmb.set('')
        self.compclicked.set(self.compoptions[1])
        self.appclicked.set(self.appoptions[7])
        self.parentnewbx.delete(0, END)
        self.parentlinkbx.delete(0, END)
        self.odioptions.clear()
        self.odispoptions.clear()
        self.desoptions.clear()
        self.primcmb['values'] = self.primoptions
        self.linkcmb.config(value=self.odioptions)
        self.link3cmb.config(value=self.odispoptions)
        self.link2cmb.config(value=self.desoptions)
        self.clear_tree()

        self.linkbtn["state"] = DISABLED
        self.searchlinkbx["state"]=DISABLED

        self.linknewbtn["state"] = DISABLED
        self.searchnewbx["state"]=DISABLED

    def check_input(self, e):
        self.value_to_search = e.widget.get()

        if self.value_to_search == "":
            self.primcmb['values'] = self.primoptions
        else:
            self.value_to_display = []
            for item in self.primoptions:
                if self.value_to_search.lower() in item.lower():
                    self.value_to_display.append(item)
            self.primcmb['values'] = self.value_to_display


    #DEFINE SELECT CLAIM RECORD FUNCTION
    def get_primary(self, event):
        self.relationid = IntVar()
        self.rllinkid = IntVar()
        self.odioptions.clear()
        self.odispoptions.clear()
        self.desoptions.clear()
        SNTree.gen.clear()
        self.linkcmb.set('')
        self.link3cmb.set('')
        self.rlcmb.set('')
        self.link2cmb.set('')

        #get primary id
        self.primary = self.primcmb.get()
        if len(self.primary) < 1:
            return False
        else:
            self.primaryid = self.primary.split(" - ")[0]
            self.relationid = 0
            self.filter_claim(self.primaryid)

            for i in db.linklistopt:

                if str(self.primaryid) == str(i[3]):
                    self.odioptions.append(str(i[2])+" - "+i[15]+" "+i[14])

                    if str(self.primaryid) == str(i[3]):
                        self.linkcmb.config(value=self.odioptions)
                    else:
                        self.linkcmb.config(value=self.odioptions)
                        self.link3cmb.config(value=self.odispoptions)
                        self.link2cmb.config(value=self.desoptions)

            self.rllinkid = self.relationid+1
            for i in self.genrloptions[self.rllinkid].keys():
                SNTree.gen.append(i)
            #print(self.gen[0])
            self.linkgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])
            self.newgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])

            #reset complete status of primary record
            for i in db.fetchstate(int(self.primaryid)):

            #set status to Complete/Incomplete
                if i[0] == "Finalisation":
                    self.appclicked.set(self.appoptions[0])
                if i[0] == "Phased":
                    self.appclicked.set(self.appoptions[1])
                if i[0] == "Settlement":
                    self.appclicked.set(self.appoptions[2])
                if i[0] == "Negotiations":
                    self.appclicked.set(self.appoptions[3])
                if i[0] == "Valuation":
                    self.appclicked.set(self.appoptions[4])
                if i[0] == "Options":
                    self.appclicked.set(self.appoptions[5])
                if i[0] == "Verification":
                    self.appclicked.set(self.appoptions[6])
                if i[0] == "Research":
                    self.appclicked.set(self.appoptions[7])
                if i[0] == "Non-compliant":
                    self.appclicked.set(self.appoptions[8])

                if i[1] == "Complete":
                    self.compclicked.set(self.compoptions[0])
                else:
                    self.compclicked.set(self.compoptions[1])


    #DEFINE SELECT FAMILY RECORD FUNCTION
    def get_odi(self, event):
        self.relationid = IntVar()
        self.rllinkid = IntVar()
        #get primary id
        self.odi = self.linkcmb.get()
        self.primary = self.primcmb.get()
        self.optionssp.clear()
        self.odispoptions.clear()
        self.desoptions.clear()
        SNTree.gen.clear()
        self.link3cmb.set('')
        self.rlcmb.set('')
        self.link2cmb.set('')


        if len(self.odi) < 1:
            return False
        else:

            self.primaryid = self.primary.split(" - ")[0]
            self.odiid = self.odi.split(" - ")[0]
            self.relationid = self.odi.split(" - ")[0][-1]
            self.rllinkid = int(self.relationid)+1

            self.my_tree.see(self.odiid)
            self.my_tree.selection_set(self.odiid)

            self.fill_parent()

            for opts in self.my_tree.get_children(self.odiid):
                self.optionssp.append(opts)
                #print(odispoptions)
            for opt in self.optionssp:
                for i in db.linklistopt:
                    #if str(rllinkid) == str(i[9]):
                    if str(opt) == str(i[2]):
                        self.odispoptions.append(str(i[2])+" - "+i[15]+" "+i[14])

                        if str(self.odiid) == str(i[2]):
                            self.link3cmb.config(value=self.odispoptions)               
                else:
                    self.link3cmb.config(value=self.odispoptions)
                    self.link2cmb.config(value=self.desoptions)

            #Link variables
            for i in self.genrloptions[self.rllinkid].keys():
                SNTree.gen.append(i)
            #print(self.gen)
            self.linkgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])
            self.newgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])

    def get_odispouse(self, event):
        self.relationid = IntVar()
        self.rllinkid = IntVar()
        #get primary id
        self.odisp = self.link3cmb.get()
        self.primary = self.primcmb.get()
        SNTree.gen.clear()
        self.options3.clear()
        self.options4.clear()
        self.options5.clear()
        self.options6.clear()
        self.options7.clear()
        self.rlcmb.set('')
        self.link2cmb.set('')

        if len(self.odisp) < 1:
            return False
        else:
            self.primaryid = self.primary.split(" - ")[0]
            self.odispid = self.odisp.split(" - ")[0]
            self.relationid = self.odisp.split(" - ")[0][-1]
            #print(relationid)
            for optsp in self.my_tree.get_children(self.odispid):
                self.options3.append(optsp)
            #print(options3)
            for opt3 in self.options3:
                if len(self.my_tree.get_children(opt3)):
                    self.options4.extend(self.my_tree.get_children(opt3))
            #print(options4)
            for opt4 in self.options4:
                if len(self.my_tree.get_children(opt4)):
                    self.options5.extend(self.my_tree.get_children(opt4))
            #print(options5)
            for opt5 in self.options5:
                if len(self.my_tree.get_children(opt5)):
                    self.options6.extend(self.my_tree.get_children(opt5))
            #print(options6)
            for opt6 in self.options6:
                if len(self.my_tree.get_children(opt6)):
                    self.options7.extend(self.my_tree.get_children(opt6))
            #print(options7)
            
            self.my_tree.see(self.odispid)
            self.my_tree.selection_set(self.odispid)

            self.fill_parent()


            #Link variables
            self.rllinkid = int(self.relationid)+1
            for i in self.genrloptions[self.rllinkid].keys():
                SNTree.gen.append(i)
            #print(rllinkid)
            #print(self.gen[0])
            self.linkgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])
            self.newgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])
            

    def get_rlkey(self, key):
        self.relationid = IntVar()
        self.rllinkid = IntVar()
        self.desoptions.clear()
        SNTree.gen.clear()
        self.link2cmb.set('')

        #get primary id
        self.genopt = self.rlcmb.get()
        self.primary = self.primcmb.get()

        if len(self.genopt) < 1:
            return False
        else:
            self.primaryid = self.primary.split(" - ")[0]
            self.relationid = self.rloptions[self.genopt]
            self.link2cmb.config(value=self.desoptions)
            
            self.options = f"self.options{str(self.relationid)}"
            for opt in eval(self.options):
                for i in db.linklistopt:
                    if str(opt) == str(i[2]):
                            
                        self.desoptions.append(str(i[2])+" - "+i[15]+" "+i[14])
                        #print(desoptions)

                        if str(self.relationid) == str(i[6]):
                            self.link2cmb.config(value=self.desoptions)
                        else:
                            self.link2cmb.config(value=self.desoptions.clear())


    def get_desc(self, event):
            self.relationid = IntVar()
            self.rllinkid = IntVar()
            #get primary id
            SNTree.gen.clear()
            self.genopt = self.rlcmb.get()
            self.des = self.link2cmb.get()
            self.primary = self.primcmb.get()

            if len(self.des) < 1:
                return False
            else:
                self.primaryid = self.primary.split(" - ")[0]
                self.desid = self.des.split(" - ")[0]
                self.relationid = self.rloptions[self.genopt]

                self.my_tree.see(self.desid)
                self.my_tree.selection_set(self.desid)

                self.fill_parent()

                #Link variables
                self.rllinkid = int(self.relationid)+1
                for i in self.genrloptions[self.rllinkid].keys():
                    SNTree.gen.append(i)
                #print(self.gen[0])
                self.linkgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])
                self.newgencmb2.config(value=self.genrloptions[self.rllinkid][SNTree.gen[0]])

    #DEFINE SELECT COMMUNITY RECORD FUNCTION
    def get_com(self, event):
        pass

    def get_mem(self, event):
        pass


    #DEFINE SELECT PROPERTY RECORD FUNCTION
    def get_prop(self, event):
        pass

    def get_land(self, event):
        pass

    #DEFINE VIEW PRIMARY RECORD FUNCTION
    def view_record(self):
        Edit_Data.estate.clear()
        Edit_Data.eview.clear()
        if len(self.my_tree.selection()) < 1:
            Edit_Data.user.append(self.userlogin.get())
            Edit_Data.estate.append("Edit")
            Edit_Data.eview.append("")
            win = Toplevel()
            Edit_Data(win)
            #messagebox.showerror("No Selection", "Select record to view")
            #return False
        else:
            try:
                self.selected = self.my_tree.selection()[0]
                #print(selected)
                self.primid = self.selected.split(".")[1]
                #print(self.primid)
                Edit_Data.user.append(self.userlogin.get())
                Edit_Data.estate.append("Edit")
                Edit_Data.eview.append(self.primid)
                win = Toplevel()
                Edit_Data(win)
            except Exception:
                messagebox.showerror("Incorrect Selection", "Select record to view")
                return False


        #Edit_Data.primcmb.set(self.my_tree.selection()[0])

    def delete_link(self):
        self.selected = self.my_tree.selection()[0]
        if len(self.selected) < 1:
            messagebox.showerror("No Selection", "Select record to delete link")
            return False
        elif len(self.my_tree.get_children(self.selected)) < 1:
            if messagebox.askokcancel("Delete Link", "Do you want to delete the link?"):
                db.removelink(self.selected.split(" - ")[0])
                db.refreshdf()
                self.refresh_lst()
                self.clear_tree()
        else:
            #print(self.my_tree.get_children(self.selected))
            messagebox.showerror("Delete Error", "Record has children linked. Delete child links first.")
            return False

    def data_entry(self):
        Edit_Data.estate.clear()
        Edit_Data.estate.append("Add")
        Edit_Data.user.append(self.userlogin.get())
        win = Toplevel()
        Edit_Data(win)

    def fam_entry(self):
        Edit_Data.estate.clear()
        Edit_Data.estate.append("Add")
        Edit_Data.user.append(self.userlogin.get())
        win = Toplevel()
        Edit_Data(win)

    def com_entry(self):
        Edit_Data.estate.clear()
        Edit_Data.estate.append("Add")
        Edit_Data.user.append(self.userlogin.get())
        win = Toplevel()
        Edit_Data(win)

    def land_entry(self):
        Edit_Data.estate.clear()
        Edit_Data.estate.append("Add")
        Edit_Data.user.append(self.userlogin.get())
        win = Toplevel()
        Edit_Data(win)

    #DEFINE TYPE STATUS FUNCTION
    def type_status(self, event):
        pass



    #DEFINE APP STATUS FUNCTION
    def app_status(self, event):
        self.primary = self.primcmb.get()
        if len(self.primary) < 1:
            return False
        else:
            self.primaryid = int(self.primary.split(" - ")[0])
            self.app = self.appclicked.get()
            db.updatestatus(self.app, self.primaryid)
            self.filter_claim(self.primaryid)

    #DEFINE COMPLETE STATUS FUNCTION
    def complete_status(self, event):
        self.primary = self.primcmb.get()
        if len(self.primary) < 1:
            return False
        else:
            self.primaryid = int(self.primary.split(" - ")[0])
            #print(self.compclicked.get())
            self.comp = self.compclicked.get()
            db.updateprogress(self.comp, self.primaryid)
            self.filter_claim(self.primaryid)


    #DEFINE USER STATUS FUNCTION
    def user_status(self, event):
        pass

    #CHECK DUPLICATE
    def check_duplicatelk(self, recordid, parentid, record, parent, claimid, generation, relationshipid, relationship, currentdate, currentuser):
        self.duplist = []
        self.linkedchild = self.my_tree.get_children(parent)
        print(self.linkedchild)
        self.record = record
        print(self.record)
        
        if self.record in self.linkedchild:
            messagebox.showerror("Duplicate Link", "This record {} is already linked to the parent".format(record))
            return False
        else:
            
            try:
                db.insertlink(recordid, parentid, record, parent, claimid, generation, relationshipid, relationship, currentdate, currentuser)

                messagebox.showinfo("Record Linked", "Record succesfully linked")
                self.print_link()
                db.refreshdf()
                self.refresh_lst()
                self.clear_tree()

                self.linkbtn["state"] = DISABLED
                self.searchlinkbx["state"]=DISABLED

            except Exception:
                messagebox.showinfo("Record Link Error", "Record not linked. Please re-select parent and try again.")
                return False

    #DEFINE LINK FUNCTION
    #self.mychecked =[]
    def link_record(self):
        self.primary = self.primcmb.get()
        self.odilink = self.linkcmb.get()
        self.odisplink = self.link3cmb.get()
        self.deslink = self.link2cmb.get()
        self.rllink = self.linkgenopt2.get()
        self.selected_linkitem = self.searchlinkbx.get()
        
        if len(self.rllink) < 1:
            messagebox.showerror("Record Link Error", "Please select relationship to link.")
            return False
        if len(self.selected_linkitem) < 1:
            messagebox.showerror("Record Link Error", "Please select record to link.")
            return False
        else:
            self.primaryid = int(self.primary.split(" - ")[0])
            self.recordid2 = (self.selected_linkitem.split(" - ")[0]).split(".")[1]
            self.cdate = datetime.datetime.now()
            self.cuser = self.userlogin.get()
            if self.rllinkid == 1:
                if len(self.odilink) < 1:
                    messagebox.showerror("No Record Selected", "Please select claim.")
                    return False
                else:
                    self.parent2 = self.primary.split(" - ")[0]
                    self.parentid2 = ""
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.rllinkid)
            elif self.rllinkid == 2:
                if len(self.odilink) < 1:
                    messagebox.showerror("No Record Selected", "Please select odi.")
                    return False
                else:
                    self.parent2 = self.odilink.split(" - ")[0]
                    self.parentid2 = self.parent2.split(".")[1]
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.parentid2)+"."+str(self.rllinkid)
            elif self.rllinkid == 3:
                if len(self.odisplink) < 1:
                    messagebox.showerror("No Record Selected", "Please select odi spouse.")
                    return False
                else:
                    self.parent2 = self.odisplink.split(" - ")[0]
                    self.parentid2 = self.parent2.split(".")[1]
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.parentid2)+"."+str(self.rllinkid)
            elif self.rllinkid in range(3,9):
                if len(self.deslink) < 1:
                    messagebox.showerror("No Record Selected", "Please select descendant.")
                    return False
                else:
                    self.parent2 = self.deslink.split(" - ")[0]
                    self.parentid2 = self.parent2.split(".")[1]
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.parentid2)+"."+str(self.rllinkid)

            #get recordid   
            #print(self.recordid2, self.parentid2, self.record2, self.parent2, self.primaryid, SNTree.gen[0], self.rllinkid, self.rllink, self.cdate, self.cuser)
            
            self.check_duplicatelk(self.recordid2, str(self.parentid2), self.record2, self.parent2, self.primaryid, SNTree.gen[0], self.rllinkid, self.rllink, self.cdate, self.cuser)
            #insert record id of contacts as child of primary id
            #db.insertlink(recordid2, linkid2, record2, link2, relation, relationid, gen, cdate)


    def new_record(self):
        self.primary = self.primcmb.get()
        self.odilink = self.linkcmb.get()
        self.odisplink = self.link3cmb.get()
        self.deslink = self.link2cmb.get()
        self.rllink = self.newgenopt2.get()
        self.selected_newitem = self.searchnewbx.get()

        if len(self.rllink) < 1:
            messagebox.showerror("Record Link Error", "Please select relationship to link.")
            return False
        if len(self.selected_newitem) < 1:
            messagebox.showerror("Record Link Error", "Please select record to link.")
            return False
        else:
            self.primaryid = int(self.primary.split(" - ")[0])
            self.recordid2 = self.selected_newitem.split(" - ")[0]
            self.cdate = datetime.datetime.now()
            self.cuser = self.userlogin.get()
            if self.rllinkid == 1:
                if len(self.primary) < 1:
                    messagebox.showerror("No Record Selected", "Please select claim.")
                    return False
                else:
                    self.parent2 = self.primary.split(" - ")[0]
                    self.parentid2 = ""
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.rllinkid)
            elif self.rllinkid == 2:
                if len(self.odilink) < 1:
                    messagebox.showerror("No Record Selected", "Please select odi.")
                    return False
                else:
                    self.parent2 = self.odilink.split(" - ")[0]
                    self.parentid2 = self.parent2.split(".")[1]
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.parentid2)+"."+str(self.rllinkid)
            elif self.rllinkid == 3:
                if len(self.odisplink) < 1:
                    messagebox.showerror("No Record Selected", "Please select odi spouse.")
                    return False
                else:
                    self.parent2 = self.odisplink.split(" - ")[0]
                    self.parentid2 = self.parent2.split(".")[1]
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.parentid2)+"."+str(self.rllinkid)
            elif self.rllinkid in range(3,9):
                if len(self.deslink) < 1:
                    messagebox.showerror("No Record Selected", "Please select descendant.")
                    return False
                else:
                    self.parent2 = self.deslink.split(" - ")[0]
                    self.parentid2 = self.parent2.split(".")[1]
                    self.record2 = str(self.primaryid)+"."+str(self.recordid2)+"."+str(self.parentid2)+"."+str(self.rllinkid)

            #print(self.recordid2, self.parentid2, self.record2, self.parent2, self.primaryid, SNTree.gen[0], self.rllinkid, self.rllink, self.cdate, self.cuser)

            try:
                #insert record id of contacts as child of primary id
                db.insertlink(self.recordid2, str(self.parentid2), self.record2, self.parent2, self.primaryid, SNTree.gen[0], self.rllinkid, self.rllink, self.cdate, self.cuser)

                #for record in df_link:
                    #print(record)

                messagebox.showinfo("Record Linked", "Record succesfully linked")
                self.print_link()
                db.refreshdf()
                self.refresh_lst()
                self.clear_tree()

                self.linknewbtn["state"] = DISABLED
                self.searchnewbx["state"]=DISABLED

            except Exception:
                messagebox.showinfo("Record Link Error", "Record not linked. Please re-select parent and try again.")
                return False



    def update_linklst(self, data):
        #clear listbox
        self.searchlinklst.delete(0, END)
        #add options
        for item in data:
            self.searchlinklst.insert(END, item)


    def fill_linklst(self, e):
        #clear entrybox
        self.searchlinkbx.delete(0, END)
        try:
            # Get index
            self.index = self.searchlinklst.curselection()[0]
            # Get selected item
            self.searchlinkbx.insert(0, self.searchlinklst.get(self.index))
            self.selected_linkitem = self.searchlinklst.get(self.index)
            #print(self.selected_linkitem) # Print tuple
            self.linkbtn["state"] = NORMAL

        except IndexError:
            pass


    def check_parentlst(self, e):
        #grab text
        self.typed = self.parentlinkbx.get()

        if self.typed == '':
            self.data = self.linkrec
        else:
            self.data = []
            for item in self.linkrec:
                if self.typed.lower() in item.lower():
                    self.data.append(item)

        self.update_linklst(self.data)
        

    def check_linklst(self, e):
        self.typed = self.searchlinkbx.get()

        if self.typed == '':
            self.data = self.linkrec
        else:
            self.data = []
            for item in self.linkrec:
                if self.typed.lower() in item.lower():
                    self.data.append(item)

        self.update_linklst(self.data)
        


    def update_newlst(self, data):
        #clear listbox
        self.searchnewlst.delete(0, END)
        #add options
        for item in data:
            self.searchnewlst.insert(END, item)

    def fill_parent(self):
        #clear entrybox
        self.parentnewbx.delete(0, END)
        self.parentlinkbx.delete(0, END)
        #insert selected item
        #try:
            # Get index
        self.selected = self.my_tree.selection()[0]

        #self.selected = self.my_tree.focus()
        #Grab record values
        #print(self.my_tree.item(self.selected))
        self.values = self.my_tree.item(self.selected, 'values')
        self.parentnewbx.insert(0, self.values[4])
        self.parentlinkbx.insert(0, self.values[4])
        #for i in self.values:

          #  print(i[4])
            # Get selected item
            #self.parentnewbx.insert(0, self.values[4])
 

        #except IndexError:
            #pass

    def fill_newlst(self, e):
        #clear entrybox
        self.searchnewbx.delete(0, END)
        #insert selected item
        try:
            # Get index
            self.index = self.searchnewlst.curselection()[0]
            # Get selected item
            self.searchnewbx.insert(0, self.searchnewlst.get(self.index))
            self.selected_newitem = self.searchnewlst.get(self.index)
            #print(self.selected_newitem) # Print tuple
            self.linknewbtn["state"] = NORMAL

        except IndexError:
            pass


    def check_newlst(self, e):
        #grab text
        self.typed = self.searchnewbx.get()

        if self.typed == '':
            self.data = self.newrec
        else:
            self.data = []
            for item in self.newrec:
                if self.typed.lower() in item.lower():
                    self.data.append(item)

        self.update_newlst(self.data)


    def clear_linkbx(self):
        self.parentlinkbx.delete(0, END)
        self.searchlinkbx.delete(0, END)
        self.linkgencmb2.set('')
        #self.data = self.linkrec
        #self.update_linklst(self.data)

        self.linkbtn["state"] = DISABLED
        self.searchlinkbx["state"]=DISABLED


    def clear_newbx(self):
        self.parentnewbx.delete(0, END)
        self.searchnewbx.delete(0, END)
        self.newgencmb2.set('')
        #self.data = self.newrec
        #self.update_newlst(self.data)
        
        self.linknewbtn["state"] = DISABLED
        self.searchnewbx["state"]=DISABLED

    def rl_linkbx(self, e):
        self.searchlinkbx["state"]=NORMAL


    def rl_newbx(self, e):
        self.searchnewbx["state"]=NORMAL

    def delete_newlist(self):
        if len(str(self.searchnewlst.curselection())) < 1:
            messagebox.showerror("No New Record Selected", "Please select new record to delete.")
            return False
        else: 
            if messagebox.askokcancel("Delete record", "Do you want to delete the record?"):
                try:
                    # Get index
                    self.index = self.searchnewlst.curselection()[0]
                    db.removelist(self.searchnewlst.get(self.index).split(" - ")[0])
                    db.refreshdf()
                    self.refresh_lst()

                except IndexError:
                    pass

    def delete_linklist(self):

        #if len(str(self.searchlinklst.curselection())) < 1:
            #messagebox.showerror("No Selection", "Select record to delete link")
            #return False
        try:
            
            self.index = self.searchlinklst.curselection()[0]
            if len(self.my_tree.get_children(self.searchlinklst.get(self.index).split(" - ")[0])) < 1:
                if messagebox.askokcancel("Delete link", "Do you want to delete the link?"):
                    db.removelink(self.searchlinklst.get(self.index).split(" - ")[0])
                    db.refreshdf()
                    self.refresh_lst()
                    self.clear_tree()
            else:
                #print(self.my_tree.get_children(self.selected))
                messagebox.showerror("Delete Error", "Record has children linked. Delete child links first.")
                return False
        
        except IndexError:
            messagebox.showerror("No Selection", "Select record to delete link")
            return False
        

    def disable_event(self):
        pass

    def update_db(self):
        db = Database('lres_tree.db')
        #self.window.after(100, self.update_db)


    def refresh_lst(self):

        #Update New Record List
        self.newrec.clear()
        self.lastcol = len(db.df_newlist.columns)-1
        for i in db.newlistopt:
            if i[self.lastcol] == "left_only":
                self.newrec.append(str(i[0])+" - "+i[4]+" "+i[3]+" ["+str(i[6])+"]")

        self.clear_newbx()
        self.update_newlst(self.newrec)

        #Update Link Record List
        self.linkrec.clear()
        for i in db.linklistopt:
            self.linkrec.append(str(i[2])+" - "+i[15]+" "+i[14]+" ["+str(i[17])+"]")

        self.clear_linkbx()
        self.update_linklst(self.linkrec)


    def print_link(self):
        print(self.recordid2, self.parentid2, self.record2, self.parent2, self.primaryid, SNTree.gen[0], self.rllinkid, self.rllink, self.cdate, self.cuser)




class Edit_Data(Frame):
    user=[]
    estate=[]
    eview=[]
    a='#249794'
    mydata=[]
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.title('Edit Data')
        self.window.geometry("620x650") # set the root dimensions
        self.window.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
        self.window.resizable(0, 0) # makes the root window fixed in size.
        self.window.configure(bg="#2f2f33")
        self.window.iconbitmap(resource_path('lres_icon.ico'))
        #self.userlogin = user

        self.s = ttk.Style()
        self.s.theme_use('default')


        self.wrapper5 = LabelFrame(self.window, text="Record Search",bg="#2f2f33", foreground="grey", font=('Calibri (Body)', 9, 'bold'), height=200)
        self.wrapper5.grid(row=0, column=0, padx=20, pady=10)

        self.wrapper4 = LabelFrame(self.window, text="Record Data", bg="#2f2f33", foreground="grey", font=('Calibri (Body)', 9, 'bold'), height=450)
        self.wrapper4.grid(row=1, column=0, padx=20, pady=10)

        #SETUP SCROLLBAR#
        self.record_scroll = Scrollbar(self.wrapper4, orient=VERTICAL)

        self.canvas4 = Canvas(self.wrapper4, width=555, height=450, bd=0, bg="#2f2f33", yscrollcommand=self.record_scroll.set)
        self.canvas4.pack(side=LEFT, fill=BOTH, expand=1)

        self.record_scroll.config(command=self.canvas4.yview)
        self.record_scroll.pack(side=RIGHT, fill=Y)

        #bind to boundary box
        self.canvas4.bind('<Configure>', lambda e: self.canvas4.configure(scrollregion = self.canvas4.bbox("all")))

        self.record_frame = Frame(self.canvas4, bg="#2f2f33")

        self.canvas4.create_window((0,0), window=self.record_frame, anchor=NW, height=935)

        self.create_editwidgets()

        self.change_state()

    def create_editwidgets(self):
        
        #self.img_refresh2 = Image.open("{}".format(sd) + "refresh2.png")
        self.img_refresh2 = Image.open(resource_path("refresh2.png"))
        self.resized2 = self.img_refresh2.resize((18,16), Image.ANTIALIAS)
        self.new_refresh2 = ImageTk.PhotoImage(self.resized2)
        

        self.recoptions=[]
        for i in db.listopt:
            self.recoptions.append(str(i[0])+" - "+i[4]+" "+i[3])

        #PRIMARY RECORD LABELS
        self.primlbl = Label(self.wrapper5, text="Select Record:" , width=17, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), anchor=W)
        self.primlbl.grid(row=0, column=0, padx=5, pady=10)

        #PRIMARY RECORD BOX
        self.primcmb = ttk.Combobox(self.wrapper5, value=self.recoptions, width=46, font=('Calibri (Body)', 8))
        self.primcmb.grid(row=0, column=1, padx=5, pady=10)
        self.primcmb.bind("<KeyRelease>", self.check_typed)

        #SEARCH BUTTON
        self.searchbtn = Button(self.wrapper5, text="Search", width=17 , command=self.search_data, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.searchbtn.grid(row=0, column=2, padx=10, pady=20)


        '''
        RECORD DATA WINDOW
        '''

        self.rid = StringVar()
        self.nod = IntVar()
        self.clm = IntVar()
        self.ln = StringVar()
        self.fn = StringVar()
        self.gen = StringVar()
        self.idn = StringVar()
        self.dob = StringVar()
        self.pas = StringVar()
        self.nat = StringVar()
        self.tel = StringVar()
        self.cel = StringVar()
        self.wrk = StringVar()
        self.eml = StringVar()
        self.pos = StringVar()
        self.add = StringVar()
        self.cit = StringVar()
        self.prv = StringVar()
        self.cnt = StringVar()
        self.zpc = StringVar()
        self.cmt = StringVar()

        self.eli = IntVar()
        self.dec = IntVar()
        self.disp = IntVar()
        self.mar = IntVar()
        self.disb = IntVar()
        self.poa = IntVar()

        self.cd = StringVar()
        self.cu = StringVar()


        self.regdob = self.window.register(self.onValidate_date)
        self.regcon = self.window.register(self.onValidate_digitmaxcon)
        self.regid = self.window.register(self.onValidate_digitmaxid)
        self.reg = self.window.register(self.onValidate)

        ##INSERT RECORDS##

        self.nameflds =[
        ("self.ln", 'Last Name:'),
        ("self.fn", 'First Name:')
        ]

        self.pobflds =[
        ("self.pas", 'Passport Number:'),
        ("self.nat", 'Nationality:')
        ]

        self.conflds =[
        ("self.tel", 'Tel Number:'),
        ("self.cel", 'Cell Number:'),
        ("self.wrk", 'Work Number:')
        ]

        self.add1flds =[
        ("self.eml", 'Email Address:'),
        ("self.pos", 'Postal Address:'),
        ("self.add", 'Physical Address:'),
        ("self.cit", 'City/Town/Place:'),
        ]

        self.add2flds =[
        ("self.cnt", 'Country:'),
        ("self.zpc", 'Postal Code:')
        ]

         

        #ENTRYS LABELS
        self.il = Label(self.record_frame, text="Record ID:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.il.grid(row=0, column=0, padx=5, pady=5)

        self.nodl = Label(self.record_frame, text="No Detail:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.nodl.grid(row=1, column=0, padx=5, pady=5)

        self.clml = Label(self.record_frame, text="Claimant:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.clml.grid(row=2, column=0, padx=5, pady=5)

        self.lnl = Label(self.record_frame, text="Last Name:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.lnl.grid(row=3, column=0, padx=5, pady=5)

        self.fnl = Label(self.record_frame, text="First Name:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.fnl.grid(row=4, column=0, padx=5, pady=5)

        self.genl = Label(self.record_frame, text="Gender:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.genl.grid(row=5, column=0, padx=5, pady=5)

        self.idnl = Label(self.record_frame, text="Identity Number:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.idnl.grid(row=6, column=0, padx=5, pady=5)

        self.dobl = Label(self.record_frame, text="DOB [yyyy/mm/dd]:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.dobl.grid(row=7, column=0, padx=5, pady=5)

        self.pasl = Label(self.record_frame, text="Passport Number:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.pasl.grid(row=8, column=0, padx=5, pady=5)

        self.natl = Label(self.record_frame, text="Nationality:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.natl.grid(row=9, column=0, padx=5, pady=5)

        self.tell = Label(self.record_frame, text="Tel Number:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.tell.grid(row=10, column=0, padx=5, pady=5)

        self.cell = Label(self.record_frame, text="Cell Number:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.cell.grid(row=11, column=0, padx=5, pady=5)

        self.wrkl = Label(self.record_frame, text="Work Number:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.wrkl.grid(row=12, column=0, padx=5, pady=5)

        self.emll = Label(self.record_frame, text="Email Address:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.emll.grid(row=13, column=0, padx=5, pady=5)

        self.posl = Label(self.record_frame, text="Postal Address:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.posl.grid(row=14, column=0, padx=5, pady=5)

        self.addl = Label(self.record_frame, text="Physical Address:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.addl.grid(row=15, column=0, padx=5, pady=5)

        self.citl = Label(self.record_frame, text="City/Town/Place:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.citl.grid(row=16, column=0, padx=5, pady=5)

        self.prvl = Label(self.record_frame, text="Province:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.prvl.grid(row=17, column=0, padx=5, pady=5)

        self.cntl = Label(self.record_frame, text="Country:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.cntl.grid(row=18, column=0, padx=5, pady=5)

        self.zpcl = Label(self.record_frame, text="Postal Code:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.zpcl.grid(row=19, column=0, padx=5, pady=5)

        self.cmtl = Label(self.record_frame, text="Comments:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=17)
        self.cmtl.grid(row=20, column=0, padx=5, pady=5)


        ##

        self.genopt={
        'Female':1,
        'Male':2
        }

        self.prvopt={
        'Eastern Cape':1,
        'Free State':2,
        'Gauteng':3,
        'KwaZulu Natal':4,
        'Limpopo':5,
        'Mpumalanga':6,
        'Northern Cape':7,
        'North West':8,
        'Western Cape':9
        }

        #ENTRY BOXES
        self.ibox = Entry(self.record_frame, textvariable=self.rid, width=8, font=('Calibri (Body)', 8))
        self.ibox.grid(row=0, column=1, padx=5, sticky=W)

        self.clearbtn = Button(self.record_frame,  image=self.new_refresh2, command=self.clear_data, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.clearbtn.grid(row=0, column=2, padx=5, sticky=E)

        self.nodbtn = Checkbutton(self.record_frame, text="", variable=self.nod, bg="#2f2f33")
        self.nodbtn.grid(row=1, column=1, padx=5, sticky=W)

        self.clmbtn = Checkbutton(self.record_frame, text="", variable=self.clm, bg="#2f2f33")
        self.clmbtn.grid(row=2, column=1, padx=5, sticky=W)

        self.lnbox = Entry(self.record_frame, textvariable=self.ln, width=50, font=('Calibri (Body)', 8))
        self.lnbox.grid(row=3, column=1, padx=5, sticky=W)

        self.fnbox = Entry(self.record_frame, textvariable=self.fn, width=50, font=('Calibri (Body)', 8))
        self.fnbox.grid(row=4, column=1, padx=5, sticky=W)

        self.gencmb = ttk.Combobox(self.record_frame, value=list(self.genopt.keys()), textvariable=self.gen, width=48, font=('Calibri (Body)', 8))
        self.gencmb.grid(row=5, column=1, padx=5, sticky=W)
        self.gencmb.set('')

        self.idnbox = Entry(self.record_frame, textvariable=self.idn, width=50, font=('Calibri (Body)', 8))
        self.idnbox.grid(row=6, column=1, padx=5, sticky=W)
        self.idnbox.config(validate = "key",validatecommand =  (self.regid,"%P"))

        #self.dobbox = Entry(self.record_frame, textvariable=self.dob, width=50, font=('Calibri (Body)', 8))
        #self.dobbox.grid(row=7, column=1, padx=5, sticky=W)


        self.dobent = DateEntry(self.record_frame, width=48, font=('Calibri (Body)', 8), date_pattern='yyyy/mm/dd', setmode='day')
        self.dobent.grid(row=7, column=1, padx=5, sticky=W) 
        self.dobent.delete(0, END) 
        self.dobent.configure(validate = 'none')
        #self.dobent.config(validate = "key",validatecommand =  (self.regdob,"%P")) 

        self.dobclearbtn = Button(self.record_frame,  text="x", command=self.cleardob, width=2, border=0,fg='white',bg="#2f2f33", activebackground='white', font=('Calibri (Body)', 8))
        self.dobclearbtn.grid(row=7, column=2, sticky=W)     

        self.pasbox = Entry(self.record_frame, textvariable=self.pas, width=50, font=('Calibri (Body)', 8))
        self.pasbox.grid(row=8, column=1, padx=5, sticky=W)

        self.natbox = Entry(self.record_frame, textvariable=self.nat, width=50, font=('Calibri (Body)', 8))
        self.natbox.grid(row=9, column=1, padx=5, sticky=W)

        self.telbox = Entry(self.record_frame, textvariable=self.tel, width=50, font=('Calibri (Body)', 8), validate="key", validatecommand=(self.regcon, '%P'))
        self.telbox.grid(row=10, column=1, padx=5, sticky=W)

        self.celbox = Entry(self.record_frame, textvariable=self.cel, width=50, font=('Calibri (Body)', 8), validate="key", validatecommand=(self.regcon, '%P'))
        self.celbox.grid(row=11, column=1, padx=5, sticky=W)

        self.wrkbox = Entry(self.record_frame, textvariable=self.wrk, width=50, font=('Calibri (Body)', 8), validate="key", validatecommand=(self.regcon, '%P'))
        self.wrkbox.grid(row=12, column=1, padx=5, sticky=W)

        self.emlbox = Entry(self.record_frame, textvariable=self.eml, width=50, font=('Calibri (Body)', 8))
        self.emlbox.grid(row=13, column=1, padx=5, sticky=W)

        self.posbox = Entry(self.record_frame, textvariable=self.pos, width=50, font=('Calibri (Body)', 8))
        self.posbox.grid(row=14, column=1, padx=5, sticky=W)

        self.addbox = Entry(self.record_frame, textvariable=self.add, width=50, font=('Calibri (Body)', 8))
        self.addbox.grid(row=15, column=1, padx=5, sticky=W)

        self.citbox = Entry(self.record_frame, textvariable=self.cit, width=50, font=('Calibri (Body)', 8))
        self.citbox.grid(row=16, column=1, padx=5, sticky=W)

        self.prvcmb = ttk.Combobox(self.record_frame, value=list(self.prvopt.keys()), textvariable=self.prv, width=48, font=('Calibri (Body)', 8))
        self.prvcmb.grid(row=17, column=1, padx=5, sticky=W)
        self.prvcmb.set('')

        self.cntbox = Entry(self.record_frame, textvariable=self.cnt, width=50, font=('Calibri (Body)', 8))
        self.cntbox.grid(row=18, column=1, padx=5, sticky=W)

        self.zpcbox = Entry(self.record_frame, textvariable=self.zpc, width=50, font=('Calibri (Body)', 8))
        self.zpcbox.grid(row=19, column=1, padx=5, sticky=W)

        #self.cmtbox = Entry(self.record_frame, textvariable=self.cmt, width=50, font=('Calibri (Body)', 8))
        #self.cmtbox.grid(row=20, column=1, padx=5, sticky=W)
        
        self.cmttxt = Text(self.record_frame, width=50, height=3, wrap=WORD, font=('Calibri (Body)', 8))
        self.cmttxt.grid(row=20, column=1, padx=5, sticky=W)

        self.cdbox = Entry(self.record_frame, textvariable=self.cd, width=15, bd=0, fg="#2f2f33" , bg="#2f2f33", font=('Calibri (Body)', 8))
        self.cdbox.grid(row=19, column=2, padx=5, pady=5)

        self.cubox = Entry(self.record_frame, textvariable=self.cu, width=15, bd=0, fg="#2f2f33" , bg="#2f2f33", font=('Calibri (Body)', 8))
        self.cubox.grid(row=20, column=2, padx=5, pady=5)

        ##STATUS BOX##
        self.statflds =[
        ("self.eli", 'Eligible:'),
        ("self.dec", 'Deceased:'),
        ("self.disp", 'Dispossessed:'),
        ("self.mar", 'Married:'),
        ("self.disb",'Disability:'),
        ("self.poa", 'Power of Attorney:')
        ]

        self.status_frame = LabelFrame(self.record_frame, bd=0, bg="#2f2f33")
        self.status_frame.grid(row=21, column=1, padx=5, pady=20, sticky=W)
        #status_frame.grid(row=21, column=0, padx=5, pady=20, columnspan=2)

        self.elil = Label(self.status_frame, text="Eligible:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=26)
        self.elil.grid(row=0, column=0, padx=5, pady=5)

        self.decl = Label(self.status_frame, text="Deceased:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=26)
        self.decl.grid(row=1, column=0, padx=5, pady=5)

        self.displ = Label(self.status_frame, text="Dispossessed:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=26)
        self.displ.grid(row=2, column=0, padx=5, pady=5)

        self.marl = Label(self.status_frame, text="Married:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=26)
        self.marl.grid(row=3, column=0, padx=5, pady=5)

        self.disbl = Label(self.status_frame, text="Disability:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=26)
        self.disbl.grid(row=4, column=0, padx=5, pady=5)
        
        self.poal = Label(self.status_frame, text="Power of Attorney:", anchor=W, bg="#2f2f33", foreground="white", font=('Calibri (Body)', 8, 'bold'), width=26)
        self.poal.grid(row=5, column=0, padx=5, pady=5)



        self.ynopt=[
        ('No', 0),
        ('Yes',1 )
        ]  


        for option, status in self.ynopt:
            self.elibtn0 = Radiobutton(self.status_frame, text="No", variable=self.eli, value=0, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.elibtn0.grid(row=0, column=1, padx=5, pady=5)

            self.elibtn1 = Radiobutton(self.status_frame, text="Yes", variable=self.eli, value=1, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.elibtn1.grid(row=0, column=2, padx=5, pady=5)

            self.decbtn0 = Radiobutton(self.status_frame, text="No", variable=self.dec, value=0, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.decbtn0.grid(row=1, column=1, padx=5, pady=5)

            self.decbtn1 = Radiobutton(self.status_frame, text="Yes", variable=self.dec, value=1, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.decbtn1.grid(row=1, column=2, padx=5, pady=5)

            self.dispbtn0 = Radiobutton(self.status_frame, text="No", variable=self.disp, value=0, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.dispbtn0.grid(row=2, column=1, padx=5, pady=5)

            self.dispbtn1 = Radiobutton(self.status_frame, text="Yes", variable=self.disp, value=1, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.dispbtn1.grid(row=2, column=2, padx=5, pady=5)

            self.marbtn0 = Radiobutton(self.status_frame, text="No", variable=self.mar, value=0, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.marbtn0.grid(row=3, column=1, padx=5, pady=5)

            self.marbtn1 = Radiobutton(self.status_frame, text="Yes", variable=self.mar, value=1, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.marbtn1.grid(row=3, column=2, padx=5, pady=5)

            self.disbbtn0 = Radiobutton(self.status_frame, text="No", variable=self.disb, value=0, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.disbbtn0.grid(row=4, column=1, padx=5, pady=5)

            self.disbbtn1 = Radiobutton(self.status_frame, text="Yes", variable=self.disb, value=1, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.disbbtn1.grid(row=4, column=2, padx=5, pady=5)

            self.poabtn0 = Radiobutton(self.status_frame, text="No", variable=self.poa, value=0, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.poabtn0.grid(row=5, column=1, padx=5, pady=5)

            self.poabtn1 = Radiobutton(self.status_frame, text="Yes", variable=self.poa, value=1, bg="light grey", bd=0, font=('Calibri (Body)', 8))
            self.poabtn1.grid(row=5, column=2, padx=5, pady=5)



        ##ENTRY BUTTONS##

        self.edit_frame = Frame(self.record_frame, bg="#2f2f33")
        #wrapper6.pack(padx=20, pady=10)
        self.edit_frame.grid(row=22,  column=1, padx=5, pady=5)

        #ADD RECORD
        self.addbtn = Button(self.edit_frame, text="Add Record", width=15, command=self.add_record, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.addbtn.grid(row=0, column=0, padx=5, pady=10)
        #self.addbtn.config(validate = "key",validatecommand =  (self.reg,"%P"))


        #UPDATE RECORD
        self.updatebtn = Button(self.edit_frame, text = "Update Record", width=15, command=self.update_record, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.updatebtn.grid(row=0, column=1, padx=5, pady=10)
        #self.updatebtn.config(validate = "key",validatecommand =  (self.reg,"%P"))

        #DELETE_RECORD
        #self.deletebtn = Button(self.edit_frame, text = "Delete Record", width=15, command=self.delete_record, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        #self.deletebtn.grid(row=0, column=2, padx=5, pady=10)
                

        #SAVE BUTTON
        self.end_frame = Frame(self.window, bg="#2f2f33")
        self.end_frame.grid(row=2, column=0, padx=20, pady=10, sticky=E)

        #RETURN BUTTON
        self.rtnbtn = Button(self.end_frame, text="Return", width=17, command=self.edit_close, border=0,fg='black',bg='light grey', activebackground='white', font=('Calibri (Body)', 8))
        self.rtnbtn.grid(row=0, column=0,  padx=5, pady=5)




        #DEFINE SAVE FUNCTION
    def file_save(self):
        db.filesave()
        messagebox.showinfo("Data Saved", "Your data has been saved successfuly.")


    def clear_data(self):

        self.ibox.delete(0, END)

        self.nodbtn.deselect()
        self.clmbtn.deselect()

        self.lnbox.delete(0, END)
        self.fnbox.delete(0, END)

        self.gencmb.set("")
        self.idnbox.delete(0, END)
        #self.dobbox.delete(0, END)
        self.dobent.delete(0, END)

        self.pasbox.delete(0, END)
        self.natbox.delete(0, END)

        self.telbox.delete(0, END)
        self.celbox.delete(0, END)
        self.wrkbox.delete(0, END)

        self.emlbox.delete(0, END)
        self.posbox.delete(0, END)
        self.addbox.delete(0, END)
        self.citbox.delete(0, END)

        self.prvcmb.set("")

        self.cntbox.delete(0, END)
        self.zpcbox.delete(0, END)

        self.cmttxt.delete(1.0, END)

        self.elibtn0.select()
        self.decbtn0.select()
        self.dispbtn0.select()
        self.marbtn0.select()
        self.disbbtn0.select()
        self.poabtn0.select()
        

        self.elibtn1.deselect()
        self.decbtn1.deselect()
        self.dispbtn1.deselect()
        self.marbtn1.deselect()
        self.disbbtn1.deselect()
        self.poabtn1.deselect()

        self.cdbox.delete(0, END)
        self.cubox.delete(0, END)

        #self.ibox["state"] = DISABLED

    def cleardob(self):
        self.dobent.delete(0, END)

    #SEARCH DATA
    def change_state(self):
        if Edit_Data.estate[0]=="Add":
            self.window.title('Add Data')
            self.primcmb["state"] = DISABLED
            self.updatebtn["state"] = DISABLED
            self.addbtn["state"] = NORMAL
            self.searchbtn["state"] = DISABLED
            self.ibox["state"] = DISABLED

        elif Edit_Data.estate[0]=="Edit":
            self.window.title('Edit Data')
            self.primcmb.set(Edit_Data.eview[0])
            #print(Edit_Data.eview[0])
            self.primcmb["state"] = NORMAL
            self.updatebtn["state"] = NORMAL
            self.addbtn["state"] = DISABLED
            self.ibox["state"] = NORMAL

    def search_data(self):
        self.clear_data()

        #self.ibox["state"] = NORMAL

        self.primary = self.primcmb.get()
        if len(self.primary) < 1:
            return False
        else:

            try:
                self.primaryid = self.primary.split(" - ")[0]

                for record in db.filterlist(int(self.primaryid)):

                    self.ibox.insert(0, record[0])
                    
                    #print(record[1])
                    if record[1]==1:
                        self.nodbtn.select()

                    #print(record[2])
                    if record[2]==1:
                        self.clmbtn.select()

                    self.lnbox.insert(0, record[3])
                    self.fnbox.insert(0, record[4])

                    self.gencmb.set(record[5])
                    self.idnbox.insert(0, record[6])
                    self.idn = record[6]
                    
                    if record[7] is None or record[7] == "":
                        self.dobent.delete(0, END)
                    else:
                        self.dobent.set_date(record[7])

                    self.pasbox.insert(0, record[14])
                    self.natbox.insert(0, record[15])

                    self.telbox.insert(0, record[11])
                    self.celbox.insert(0, record[16])
                    self.wrkbox.insert(0, record[17])

                    self.emlbox.insert(0, record[18])
                    self.posbox.insert(0, record[19])
                    self.addbox.insert(0, record[20])
                    self.citbox.insert(0, record[21])

                    self.prvcmb.set(record[22])

                    self.cntbox.insert(0, record[23])
                    self.zpcbox.insert(0, record[24])

                    self.cmttxt.insert(1.0, record[28])


                    if record[9] == 0:
                        self.elibtn0.select()
                    if record[9] == 1:
                        self.elibtn1.select()

                    if record[8] == 0:
                        self.decbtn0.select()
                    if record[8] == 1:
                        self.decbtn1.select()

                    if record[10] == 0:
                        self.dispbtn0.select()
                    elif record[10] == 1:
                        self.dispbtn1.select()

                    if record[25] == 0:
                        self.marbtn0.select()
                    if record[25] == 1:
                        self.marbtn1.select()

                    if record[26] == 0:
                        self.disbbtn0.select()
                    if record[26] == 1:
                        self.disbbtn1.select()

                    if record[27] == 0:
                        self.poabtn0.select()
                    if record[27] == 1:
                        self.poabtn1.select()
                            
                    self.cdbox.insert(0, record[12])
                    self.cubox.insert(0, record[13])

            except ValueError:
                messagebox.showerror("Invalid Search", "No record found, please select record from dropdown")
                return None

            except IndexError:
               return None



    def check_typed(self, e):
        self.value_to_search = e.widget.get()

        if self.value_to_search == "":
            self.primcmb['values'] = self.recoptions
        else:
            self.value_to_display = []
            for item in self.recoptions:
                if self.value_to_search.lower() in item.lower():
                    self.value_to_display.append(item)
            self.primcmb['values'] = self.value_to_display


    def check_duplicateinls(self, BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
        IDNo, DOB, Deceased, Eligible, Dispossessed, HomeNumber, 
        CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
        EmailAddress, PostalAddress, PhysicalAddress,
        City, Province, Country, ZipCode, Married, Disabled, 
        POA, Comments):

        self.duplistidno=[]
        self.duplistid=[]

        for i in db.listopt:
            if len(str(i[6])) < 1:
                pass
            else:
                self.duplistidno.append(i[6])

        if IDNo in self.duplistidno:
            messagebox.showerror("Duplicate Record", "This ID number {} already exists in the database".format(IDNo))
            return False
        else:
            db.insertlist(BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, Dispossessed, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments)


            messagebox.showinfo("Record Added", "New record succesfully added")
            self.print_record()
            db.refreshdf()
            self.clear_data()
            
        

    #DEFINE INSERT FUNCTION
    def add_record(self):
        if len(str(self.rid.get())) < 1:

            if self.onValidate() and self.onValidate_date():
                #self.ibox["state"] = DISABLED
                self.rid_last = db.df_list.values[-1].tolist()[0]
                self.ridnew = self.rid_last+1
                self.ibox.insert(0, self.ridnew)

                self.cmt = self.cmttxt.get(1.0, END)

                
                if len(str(self.ridnew)) < 1 or len(self.ln.get()) < 1:
                    messagebox.showerror("Required Fields", "'Last Name' field cannot be empty.")
                    return False
                else:
                    Edit_Data.mydata.clear()
                    self.cdate = datetime.datetime.now()
                    self.cuser = Edit_Data.user[0]
                    self.check_duplicateinls(self.ridnew, self.nod.get(), self.clm.get(), self.lnbox.get(),
                    self.fnbox.get(), self.gencmb.get(), self.idnbox.get(), self.dobent.get_date(), 
                    self.dec.get(), self.eli.get(), self.disp.get(), self.telbox.get(), self.cdate, self.cuser, 
                    self.pasbox.get(), self.natbox.get(), self.celbox.get(), self.wrkbox.get(), self.emlbox.get(),
                    self.posbox.get(), self.addbox.get(), self.citbox.get(), self.prvcmb.get(), self.cntbox.get(),
                    self.zpcbox.get(), self.mar.get(), self.disb.get(), self.poa.get(), self.cmttxt.get(1.0, END))


    def check_duplicateupls(self, BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
        IDNo, DOB, Deceased, Eligible, Dispossessed, HomeNumber, 
        CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
        EmailAddress, PostalAddress, PhysicalAddress,
        City, Province, Country, ZipCode, Married, Disabled, 
        POA, Comments, MDate, MUser):

        self.duplist=[]

        for i in db.listopt:
            if len(str(i[6])) < 1:
                pass
            else:
                self.duplist.append(i[6])

        if IDNo in self.duplist:
            #print(IDNo)
            messagebox.showerror("Duplicate Record", "This ID number {} already exists in the database".format(IDNo))
            return False
        else:
            db.updatelist(BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, Dispossessed, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments, MDate, MUser)


            messagebox.showinfo("Record Updated", "Record succesfully updated")
            self.print_record()
            db.refreshdf()
            self.clear_data()
            

    #DEFINE UPDATE RECORD FUNCTION
    def update_record(self):
        if self.onValidate() and self.onValidate_date():
            self.rid2 = self.rid.get()
            self.cmt = self.cmttxt.get(1.0, END)

            if len(str(self.rid2)) < 1:
                messagebox.showerror("No Record Selected", "Please select record.")
                return False
            else:
                if len(self.ln.get()) < 1:
                    messagebox.showerror("Required Fields", "'Last Name' field cannot be empty.")
                    return False
                else:
                    self.mdate = datetime.datetime.now()
                    self.muser = Edit_Data.user[0]
                    if messagebox.askyesno("Confirm Update?", "Are you sure you want to save changes to this record?"):
                        if self.idn == self.idnbox.get() or self.idnbox.get()=="":
                            db.updatelist(self.rid2, self.nod.get(), self.clm.get(), self.lnbox.get(),
                            self.fnbox.get(), self.gencmb.get(), self.idnbox.get(), self.dobent.get_date(), self.dec.get(),
                            self.eli.get(), self.disp.get(), self.telbox.get(), self.cdbox.get(), self.cubox.get(), 
                            self.pasbox.get(), self.natbox.get(), self.celbox.get(), self.wrkbox.get(), self.emlbox.get(),
                            self.posbox.get(), self.addbox.get(), self.citbox.get(), self.prvcmb.get(), self.cntbox.get(),
                            self.zpcbox.get(), self.mar.get(), self.disb.get(), self.poa.get(), self.cmttxt.get(1.0, END),
                            self.mdate, self.muser)

                            messagebox.showinfo("Record Updated", "Record succesfully updated")
                            
                            self.print_record()
                            db.refreshdf()
                            self.clear_data()

                        else: 
                            self.check_duplicateupls(self.rid2, self.nod.get(), self.clm.get(), self.lnbox.get(),
                            self.fnbox.get(), self.gencmb.get(), self.idnbox.get(), self.dobent.get_date(), self.dec.get(),
                            self.eli.get(), self.disp.get(), self.telbox.get(), self.cdbox.get(), self.cubox.get(), 
                            self.pasbox.get(), self.natbox.get(), self.celbox.get(), self.wrkbox.get(), self.emlbox.get(),
                            self.posbox.get(), self.addbox.get(), self.citbox.get(), self.prvcmb.get(), self.cntbox.get(),
                            self.zpcbox.get(), self.mar.get(), self.disb.get(), self.poa.get(), self.cmttxt.get(1.0, END),
                            self.mdate, self.muser)


    #DEFINE DELETE RECORD FUNCTION
    def delete_record(self):
        self.rid2 = self.ibox.get()
        if len(str(self.rid2)) < 1:
            self.clear_data()
            #messagebox.showerror("New Record", "Record not saved")
            return False
        else:
            print(db.fetchid(self.rid2))
            if len(db.fetchid(self.rid2))<1:
                if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this record?"):
                    db.removelist(self.rid2)
                    db.refreshdf()
                    self.clear_data()
            else:
                messagebox.showerror("Delete Error", "This record {} has child links. Please delete linked children first".format(self.rid2))
                return False






    ##Validation##

    def onValidate_digitmaxid(self, e):
        if len(e) == 0 or len(e) <= 13 and e.isdigit():  # 10 characters
            return True
        else:
            messagebox.showerror("Invalid Entry", "Identity number has 13 digits.")
            return False

    def onValidate_digitmaxcon(self, e):
        if len(e) == 0 or len(e) <= 10 and e.isdigit():  # 10 characters
            return True
        else:
            messagebox.showerror("Invalid Entry", "Contact Number has 10 digits.")
            return False

    def onValidate_date(self):
        if self.dobent.get_date() is not None: 
            self.systemdate = datetime.date.today()
            
            #self.birthdate = datetime.datetime.combine(self.dobent.get_date(), datetime.min.time())
            self.birthdate = self.dobent.get_date()
            
            if self.birthdate < self.systemdate:
                return True

            else:   
                messagebox.showerror("Invalid Entry", "Date of birth cannot be after today's date.")
                #self.dobent.delete(0, END) 
                return False

        else:
            if self.dobent.get_date() is None:
                print("empty")
                return True

            '''     
            try:
                self.birthdate = datetime.datetime.strptime(self.dobbox.get(), '%Y-%m-%d')
            except:
                messagebox.showerror("Invalid Entry", "Date of birth format is 'yyyy-mm-dd'")
                return False
            else:
                if self.birthdate < self.systemdate:
                    return True
                else:
                    messagebox.showerror("Invalid Entry", "Date of birth cannot be after today's date.")
            '''

    def onValidate(self):
        try:
            if len(self.idnbox.get()) == 0 or len(self.idnbox.get()) == 13 and self.idnbox.get().isdigit():  # 10 characters
                if len(self.telbox.get()) == 0 or len(self.telbox.get()) == 10 and self.telbox.get().isdigit():  # 10 characters
                    if len(self.celbox.get()) == 0 or len(self.celbox.get()) == 10 and self.celbox.get().isdigit():  # 10 characters
                        if len(self.wrkbox.get()) == 0 or len(self.wrkbox.get()) == 10 and self.wrkbox.get().isdigit():  # 10 characters
                            return True
                        else:
                            messagebox.showerror("Invalid Entry", "Contact Number must have 10 digits.")
                            return False
                    else:
                        messagebox.showerror("Invalid Entry", "Contact Number must have 10 digits.")
                        return False
                else:
                    messagebox.showerror("Invalid Entry", "Contact Number must have 10 digits.")
                    return False
            else:
                messagebox.showerror("Invalid Entry", "Identity number must have 13 digits.")
                return False

        except:
            return False

    def print_record(self):
        print(self.ibox.get(), self.nod.get(), self.clm.get(), self.lnbox.get(),
                self.fnbox.get(), self.gencmb.get(), self.idnbox.get(), self.dobent.get_date(), self.dec.get(),
                self.eli.get(), self.disp.get(), self.telbox.get(), self.cdbox.get(), self.cubox.get(), 
                self.pasbox.get(), self.natbox.get(), self.celbox.get(), self.wrkbox.get(), self.emlbox.get(),
                self.posbox.get(), self.addbox.get(), self.citbox.get(), self.prvcmb.get(), self.cntbox.get(),
                self.zpcbox.get(), self.mar.get(), self.disb.get(), self.poa.get(), self.cmttxt.get(1.0, END))


    def edit_close(self):
        self.window.destroy()


class Claim_Data(Frame):
    user = []
    mydata = []
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.geometry("250x90")
        self.window.title('Claim Data')
        self.window.geometry("500x500") # set the root dimensions
        self.window.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
        self.window.resizable(0, 0) # makes the root window fixed in size.
        self.window.iconbitmap(resource_path('lres_icon.ico'))
        #self.top.configure(bg="#2f2f33")
        #self.user = StringVar()

        self.s = ttk.Style()
        self.s.theme_use('default')

        # Frame for TreeView
        self.frame1 = LabelFrame(self.window, text="Excel Data")
        self.frame1.place(height=250, width=500)

        # Frame for open file dialog
        self.file_frame = LabelFrame(self.window, text="Open File")
        self.file_frame.place(height=100, width=400, rely=0.65, relx=0.10)

        # Buttons
        self.button1 = Button(self.file_frame, text="Browse File", width=10, command=lambda: self.file_dialog())
        self.button1.place(rely=0.65, relx=0.10)

        self.button2 = Button(self.file_frame, text="View File", width=10,  command=lambda: self.view_excel_data())
        self.button2.place(rely=0.65, relx=0.40)

        self.button3 = Button(self.file_frame, text="Upload File", width=10, command=lambda: self.upload_excel_data())
        self.button3.place(rely=0.65, relx=0.70)

        # The file/file path text
        self.label_file = Label(self.file_frame, text="No File Selected")
        self.label_file.place(rely=0, relx=0)


        ## Treeview Widget
        self.tv1 = ttk.Treeview(self.frame1)
        self.tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        self.treescrolly = Scrollbar(self.frame1, orient="vertical", command=self.tv1.yview) # command means update the yaxis view of the widget
        self.treescrollx = Scrollbar(self.frame1, orient="horizontal", command=self.tv1.xview) # command means update the xaxis view of the widget
        self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set) # assign the scrollbars to the Treeview Widget
        self.treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        self.treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


    def file_dialog(self):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        self.filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select A File",
                                              filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
        self.label_file["text"] = self.filename
        return None


    def view_excel_data(self):
        """If the file selected is valid this will load the file into the Treeview"""
        if len(self.label_file["text"])<1:
            messagebox.showerror("Select File", "No file selected to view.")
        else:
            self.file_path = self.label_file["text"]
            try:
                self.excel_filename = r"{}".format(self.file_path)
                self.df = pd.read_excel(self.excel_filename).fillna("")

            except ValueError:
                messagebox.showerror("Information", "The file you have chosen is invalid")
                return None
            except FileNotFoundError:
                messagebox.showerror("Information", f"No such file as {self.file_path}")
                return None

            Claim_Data.mydata.clear()
            self.clear_data()
            
            self.tv1['columns'] = ('No.', 'ClaimName', 'Status', 'ClaimFileNumber', 'Progress', 'ClaimantName', 'ClaimantReference', 'ProjectName', 'Province', 'District', 'Comment', 'EstimatedBudget', 'EstimatedOptions', 'LandType', 'ClaimType', 'Rule5Status', 'Rule5ApproveDate', 'RegistryNumber')
            
            self.tv1["show"] = "headings"
            for column in self.tv1["columns"]:
                self.tv1.heading(column, text=column) # let the column heading = column name

            self.df_rows = self.df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in self.df_rows:
                self.tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
                Claim_Data.mydata.append(row)
            return None

    def clear_data(self):
        Claim_Data.mydata.clear()
        self.tv1.delete(*self.tv1.get_children())
        return None

    def upload_excel_data(self):
         if len(Claim_Data.mydata) < 1:
            messagebox.showerror("Load Error", "No data to load.")
         else:
            self.loadrows = self.df.values.tolist()
            self.duplist=[]
            self.claim_last = db.df_claim.values[-1].tolist()[0]
            self.claimnew = self.claim_last + 1
            self.cdate = datetime.datetime.now()
            self.cuser = Claim_Data.user[0]
            for i in db.claimopt:
                #print("Duplicate ID:" + i[6])
                self.duplist.append(i[1]+" - "+i[3]+" - "+i[8])
            for record in self.loadrows:
                dupcheck = record[1]+" - "+record[3]+" - "+record[8]
                if dupcheck in self.duplist and dupcheck!="":
                    print(dupcheck)
                    #print("Duplicate ID:" + i[6])
                    pass
                else:
                    db.insertclaim(self.claimnew, record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11], record[12], record[13], record[14], record[15], record[16], record[17], self.cdate, self.cuser,"", "")
                    self.claimnew +=1
                    #print(record[0])
                        
            messagebox.showinfo("Data Uploaded", "Your data has been uploaded successfuly.")
            db.refreshdf()
            self.window.destroy()

    def exportcsv(self):
        if len(self.exprows) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        else:
            db.exportclaim_csv(self.exprows)
            messagebox.showinfo("Data Exported", "Your data has been exported successfuly.")


    def click_load(self):
        """calls login page when clicked on login button"""
        win = Toplevel()
        SNTree(win)
        self.window.withdraw()
        win.deiconify()


class DateEntry(DateEntry):
            def get_date(self):
                if not self.get():
                    return None
                self._validate_date()
                return self.parse_date(self.get())





def win():
    window = Tk()
    StartApp(window)
    #window.after_idle(SNTree.update_db)
    window.mainloop()




if __name__ == '__main__':
    win()




