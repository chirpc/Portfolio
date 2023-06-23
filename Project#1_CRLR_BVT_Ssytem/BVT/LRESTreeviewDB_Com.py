from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import datetime
import csv
import os


sd = '//researchdata.uct.ac.za/LRES/Survey_Assistants/LRES_Database/PyDatabase/'

'''
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
'''

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Database_Com:
    #def __init__(self, infile, claimsheet, listsheet, linksheet, usersheet, db):
    def __init__(self, db):
        #\\researchdata.uct.ac.za\LRES\Survey_Assistants\LRES_Database\PyDatabase
        
        ##SETUP DATABASE##
        #print(resource_path(db))
        #self.conn = sqlite3.connect(resource_path(db))
        self.conn = sqlite3.connect("{}".format(sd) + db)

        self.cur = self.conn.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS tblMemList (MemID INTEGER PRIMARY KEY, Claimant integer, LastName text, FirstName text, Gender text, 
                    IDNo text, DOB text, Deceased integer, Eligible integer, HomeNumber text, 
                    CDate text, CUser text, PassportNo text, Nationality text, CellNumber text, WorkNumber text, 
                    EmailAddress text, PostalAddress text, PhysicalAddress text,  City text, Province text, 
                    Country text, ZipCode text, Married integer, Disabled integer, POA integer, Comments text, 
                    Member_No text, MDate text, MUser text)""")
        conn.commit()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS tblComMemLink (ComID integer,MemID integer,PhaseID integer,ODH text,Relationship text,HHID integer,GroupID integer,CDate text,MDate text,CUser text,MUser text)")
        conn.commit()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS tblComList (ComID INTEGER PRIMARY KEY,ComName text,ComType text,ChairLastName text,ChairFirstName text,RegNo text,ChairIDNo text,ChairContactNo text,Comments text,ChairAddress text,ChairDeceased integer,ChairGender text,CDate text,MDate text,CUser text,MUser text)")
        conn.commit()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS tblClaimComLink (ComID integer, ClaimID integer, CDate text, MDate text, CUser text, MUser text)")
        conn.commit()


        self.querymem = "SELECT * FROM tblMemList"
        self.mem_row = self.cur.execute(self.querymem).fetchall()
        self.querycommem = "SELECT * FROM tblComMemLink"
        self.commem_row = self.cur.execute(self.querycommem).fetchall()
        self.querycom = "SELECT * FROM tblComList"
        self.com_row = self.cur.execute(self.querycom).fetchall()
        self.queryclaimcom = "SELECT * FROM tblClaimComLink"
        self.user_claimcom = self.cur.execute(self.queryclaimcom).fetchall()

        self.col_mem = ['MemID','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Member_No','Comments','MDate','MUser']
        self.df_mem = pd.DataFrame(self.mem_row, columns=self.col_mem).fillna("")
        self.col_commem = ['ComID','MemID','PhaseID','GroupID','HHID','ID','PID','ODH','Relationship','CDate','MDate','CUser','MUser']
        self.df_commem = pd.DataFrame(self.commem_row, columns=self.col_commem).fillna("")
        self.col_com = ['ComID','ComName','ComType','ChairLastName','ChairFirstName','RegNo','ChairIDNo','ChairContactNo','Comments','ChairAddress','ChairDeceased','ChairGender','CDate','MDate','CUser','MUser']
        self.df_com = pd.DataFrame(self.com_row, columns=self.col_com).fillna("")
        self.col_claimcom = ['ComID','ClaimID','ID','CDate','MDate','CUser','MUser']
        self.df_claimcom = pd.DataFrame(self.claimcom_row, columns=self.col_claimcom).fillna("")
    
        #creating count for recordid
        #self.rid_last = self.df_list.values[-1].tolist()[0]
        #self.rid_last = 20000
        #self.rid_last +=1

        self.commem_last = len(self.df_commem.values.tolist())
        self.claimcom_last = len(self.df_claimcom.values.tolist())

        #pulling values from dataframe
        self.memopt = self.df_mem.values.tolist()
        self.commemopt = self.df_commem.values.tolist()
        self.comopt = self.df_com.values.tolist()
        self.claimcomopt = self.df_claimcom.values.tolist()

        #merging dataframe
        self.df_linkcommem = pd.merge(self.df_commem, self.df_mem, how="left", on=["MemID"], indicator=True)
        self.df_linkcommem.sort_values(by=['ComID','MemID','HHID','PhaseID'], inplace=True, ascending=False)
        self.linkcommemopt = self.df_linkcommem.values.tolist()

        self.df_newmemcom = pd.merge(self.df_mem, self.df_commem, how="left", on=["MemID"], indicator=True)
        self.df_newmemcom.sort_values(by=['MemID'], inplace=True, ascending=False)
        self.newmemcomopt = self.df_newmemcom.values.tolist()
        print(df_newmemcom.info())



    def fetchmemlist(self):
        self.querylist = "SELECT * FROM tblMemList"
        self.cur.execute(self.querylist)
        listrows = self.cur.fetchall()
        return listrows

    def fetchcommemlink(self):
        self.querylink = "SELECT * FROM tblComMemLink"
        self.cur.execute(self.querylink)
        linkrows = self.cur.fetchall()
        return linkrows

    def fetchcomlist(self):
        self.querylist = "SELECT * FROM tblComList"
        self.cur.execute(self.querylist)
        listrows = self.cur.fetchall()
        return listrows

    def fetchclaimcomlink(self):
        self.querylink = "SELECT * FROM tblClaimComLink"
        self.cur.execute(self.querylink)
        linkrows = self.cur.fetchall()
        return linkrows

    def fetchclaimcommemlistlink(self):
        self.querylistlink = "SELECT tblMemList.MemID, tblComMemLink.HHID, tblMemList.FirstName, tblMemList.LastName, tblComMemLink.Relationship, tblMemList.Claimant, \
                tblComMemLink.ID, tblComMemLink.PID, tblComMemLink.ComID, tblMemList.FirstName & ' ' & tblMemList.LastName & IIF(tblMemList.Deceased = 1, ' (D)', '') AS MemName, \
                tblComMemLink.ODH, tblComMemLink.PhaseID, tblComMemLink.GroupID, tblMemList.Deceased, tblComList.ComName, tblComList.ComType, tblClaimComLink.ClaimID \
                FROM (tblComList LEFT JOIN (tblComMemLink LEFT JOIN tblMemList ON tblComMemLink.MemID = tblMemList.MemID) ON tblComList.ComID = tblComMemLink.ComID) \
                INNER JOIN (tblClaimList LEFT JOIN tblClaimComLink ON tblClaimList.ClaimID = tblClaimComLink.ClaimID) ON tblComList.ComID = tblClaimComLink.ComID \
                ORDER BY tblComMemLink.PhaseID, tblComMemLink.GroupID, tblMemList.MemID"     
        self.cur.execute(self.querylistlink)
        linkchildrows = self.cur.fetchall()
        return linkchildrows


    def fetchmemid(self, MemID):
        self.cur.execute("SELECT DISTINCT tblComMemLink.MemID FROM tblComMemLink WHERE tblComMemLink.HHID = ?",
            (str(MemID),))
        idrows = self.cur.fetchall()
        return idrows


    def filtermemlist(self, MemID):
        self.cur.execute("SELECT * FROM tblMemList WHERE tblMemList.MemID = ?", 
            (MemID,))
        listrows = self.cur.fetchall()
        return listrows

    def filtercomlist(self, ComID):
        self.cur.execute("SELECT * FROM tblComList WHERE tblComList.ComID = ?", 
            (ComID,))
        listrows = self.cur.fetchall()
        return listrows

    def filterclaimcommemlink(self, ClaimID):
        self.cur.execute("SELECT tblMemList.MemID, tblComMemLink.HHID, tblMemList.FirstName, tblMemList.LastName, tblComMemLink.Relationship, tblMemList.Claimant, \
                tblComMemLink.ID, tblComMemLink.PID, tblComMemLink.ComID, tblMemList.FirstName & ' ' & tblMemList.LastName & IIF(tblMemList.Deceased = 1, ' (D)', '') AS MemName, \
                tblComMemLink.ODH, tblComMemLink.PhaseID, tblComMemLink.GroupID, tblMemList.Deceased, tblComList.ComName, tblComList.ComType, tblClaimComLink.ClaimID \
                FROM (tblComList LEFT JOIN (tblComMemLink LEFT JOIN tblMemList ON tblComMemLink.MemID = tblMemList.MemID) ON tblComList.ComID = tblComMemLink.ComID) \
                INNER JOIN (tblClaimList LEFT JOIN tblClaimComLink ON tblClaimList.ClaimID = tblClaimComLink.ClaimID) ON tblComList.ComID = tblClaimComLink.ComID \
                ORDER BY tblComMemLink.PhaseID, tblComMemLink.GroupID, tblMemList.MemID", 
                (ClaimID,))
        linkchildrows = self.cur.fetchall()
        return linkchildrows
 

    def insertmemlist(self, MemID, Claimant, LastName, FirstName, Gender, 
			    	IDNo, DOB, Deceased, Eligible, 
			    	HomeNumber, CDate, CUser, PassportNo=None, Nationality=None, 
			    	CellNumber=None, WorkNumber=None, EmailAddress=None, PostalAddress=None, 
			    	PhysicalAddress=None,  City=None, Province=None, Country=None, ZipCode=None, 
			    	Married=None, Disabled=None, POA=None, Comments=None, Member_No=None, MDate=None, MUser=None):
        self.cur.execute("INSERT INTO tblMemList VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (MemID, Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments, Member_No, MDate, MUser))
        self.conn.commit()

    def insertcomlist(self, ComID,ComName,ComType,ChairLastName=None,
                    ChairFirstName=None,RegNo=None,ChairIDNo=None,ChairContactNo=None,Comments=None,
                    ChairAddress=None,ChairDeceased=None,ChairGender=None,CDate,MDate=None,CUser,MUser=None):
        self.cur.execute("INSERT INTO tblMemList VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ComID,ComName,ComType,ChairLastName,
                    ChairFirstName,RegNo,ChairIDNo,ChairContactNo,Comments,
                    ChairAddress,ChairDeceased,ChairGender,CDate,MDate,CUser,MUser))
        self.conn.commit()

    def insertcommemlink(self, ComID,MemID,PhaseID,GroupID,HHID,ID,PID,ODH,Relationship,CDate,MDate,CUser=None,MUser=None):
        self.cur.execute("INSERT INTO tblComMemLink  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ComID,MemID,PhaseID,GroupID,HHID,ID,PID,ODH,Relationship,CDate,MDate,CUser,MUser))
        self.conn.commit()

    def insertclaimmemlink(self, ComID,ClaimID,ID,CDate,MDate=None,CUser,MUser=None):
        self.cur.execute("INSERT INTO tblComMemLink  VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ComID,ClaimID,ID,CDate,MDate,CUser,MUser))
        self.conn.commit()


    def updatememlist(self, MemID, Claimant, LastName, FirstName, Gender, 
                    IDNo, DOB, Deceased, Eligible, 
                    HomeNumber, CDate, CUser, PassportNo=None, Nationality=None, 
                    CellNumber=None, WorkNumber=None, EmailAddress=None, PostalAddress=None, 
                    PhysicalAddress=None,  City=None, Province=None, Country=None, ZipCode=None, 
                    Married=None, Disabled=None, POA=None, Comments=None, Member_No=None, MDate=None, MUser=None):
        self.cur.execute("UPDATE tblComList SET  Claimant=?, LastName=?, FirstName=?, Gender=?, \
            IDNo=?, DOB=?, Deceased=?, Eligible=?, HomeNumber=?, CDate=?, CUser=?, PassportNo=?, \
            Nationality=?, CellNumber=?, WorkNumber=?, EmailAddress=?, PostalAddress=?, PhysicalAddress=?,  City=?, \
            Province=?, Country=?, ZipCode=?, Married=?, Disabled=?, POA=?, Comments=?, Member_No=?, MDate=?, MUser=? \
            WHERE ComID=?",
            (Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments, Member_No, MDate, MUser, MemID))
        self.conn.commit()

    def updatcomlist(self, MemID, Claimant, LastName, FirstName, Gender, 
                    IDNo, DOB, Deceased, Eligible, 
                    HomeNumber, CDate, CUser, PassportNo=None, Nationality=None, 
                    CellNumber=None, WorkNumber=None, EmailAddress=None, PostalAddress=None, 
                    PhysicalAddress=None,  City=None, Province=None, Country=None, ZipCode=None, 
                    Married=None, Disabled=None, POA=None, Comments=None, Member_No=None, MDate=None, MUser=None):
        self.cur.execute("UPDATE tblComList SET  Claimant=?, LastName=?, FirstName=?, Gender=?, \
            IDNo=?, DOB=?, Deceased=?, Eligible=?, HomeNumber=?, CDate=?, CUser=?, PassportNo=?, \
            Nationality=?, CellNumber=?, WorkNumber=?, EmailAddress=?, PostalAddress=?, PhysicalAddress=?,  City=?, \
            Province=?, Country=?, ZipCode=?, Married=?, Disabled=?, POA=?, Comments=?, Member_No=?, MDate=?, MUser=? \
            WHERE ComID=?",
            (Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments, Member_No, MDate, MUser, MemID))
        self.conn.commit()


    def removememlist(self, MemID):
        self.cur.execute("DELETE FROM tblMemList WHERE MemID=?", 
            (MemID,))
        self.conn.commit()

    def removememlist(self, ComID):
        self.cur.execute("DELETE FROM tblComList WHERE ComID=?", 
            (ComID,))
        self.conn.commit()

    def removecommemlink(self, ID):
        self.cur.execute("DELETE FROM tblComMemLink WHERE ID=?", 
            (ID,))
        self.conn.commit()

    def removeclaimcomlink(self, ID):
        self.cur.execute("DELETE FROM tblClaimComLink WHERE ID=?", 
            (ID,))
        self.conn.commit()


    def fileexport(self, infile):
    	self.querylink = "SELECT * FROM tblClaimFamLink"
    	self.link_row = self.cur.execute(self.querylink).fetchall()
    	self.querylist = "SELECT * FROM tblFamList"
    	self.list_row = self.cur.execute(self.querylist).fetchall()
    	self.queryclaim = "SELECT * FROM tblClaimList"
    	self.claim_row = self.cur.execute(self.queryclaim).fetchall()

    	#transform to dataframe for analysis
    	self.claim_out = pd.DataFrame(self.claim_row, columns=self.df_claim.columns)
    	self.list_out = pd.DataFrame(self.list_row, columns=self.df_list.columns)
    	self.link_out = pd.DataFrame(self.link_row, columns=self.df_link.columns)

    	self.writer = pd.ExcelWriter(infile, engine='openpyxl')

    	#output to excel file
    	self.claim_out.to_excel(self.writer, sheet_name='ClaimList', index=False)
    	self.list_out.to_excel(self.writer, sheet_name='FamList', index=False)
    	self.link_out.to_excel(self.writer, sheet_name='ClaimFamLink', index=False)

    	self.writer.save()
    	self.writer.close()

    def exportclaim_csv(self, mydata):
        #self.exp_header = ['ClaimID', 'ClaimName', 'Status', 'ClaimFileNumber', 'Progress', 'ClaimantName', 'ClaimantReference', 'ProjectName', 'Province', 'District', 'Comment', 'EstimatedBudget', 'EstimatedOptions', 'LandType', 'ClaimType', 'Rule5Status', 'Rule5ApproveDate', 'RegistryNumber', 'CDate', 'CUser', 'MDate', 'MUser']
        self.cdate = datetime.datetime.now() 
        self.filename = "{}".format(sd) + "ClaimList" + "{}".format(self.cdate) + ".csv"
        with open(self.filename, mode='w', newline='',  encoding='utf-8') as self.myfile:
            self.exp_writer = csv.writer(self.myfile, delimiter=';')
            self.exp_writer.writerow(self.col_claim)
            for record in mydata:
                self.exp_writer.writerow(record)


    def exportlist_csv(self, mydata):
        #self.exp_header = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
        self.cdate = datetime.datetime.now()
        self.filename = "{}".format(sd) + "FamList" + "{}".format(self.cdate) + ".csv"
        with open(self.filename, mode='w', newline='',  encoding='utf-8') as self.myfile:
            self.exp_writer = csv.writer(self.myfile, delimiter=';')
            self.exp_writer.writerow(self.col_list)
            for record in mydata:
                self.exp_writer.writerow(record)

    def exportlink_csv(self, mydata):
        #self.exp_header = ['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser']
        self.cdate = datetime.datetime.now()
        self.filename = "{}".format(sd) + "ClaimFamLink" + "{}".format(self.cdate) + ".csv"
        with open(self.filename, mode='w', newline='', encoding='utf-8') as self.myfile:
            self.exp_writer = csv.writer(self.myfile, delimiter=';')
            self.exp_writer.writerow(self.col_link)
            for record in mydata:
                self.exp_writer.writerow(record)


    def exportuser_csv(self, mydata):
        #self.exp_header = ['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser']
        self.cdate = datetime.datetime.now()
        self.filename = "{}".format(sd) + "UserList" + "{}".format(self.cdate) + ".csv"
        with open(self.filename, mode='w', newline='', encoding='utf-8') as self.myfile:
            self.exp_writer = csv.writer(self.myfile, delimiter=';')
            self.exp_writer.writerow(self.col_link)
            for record in mydata:
                self.exp_writer.writerow(record)


    def refreshdf(self):

        self.querymem = "SELECT * FROM tblMemList"
        self.mem_row = self.cur.execute(self.querymem).fetchall()
        self.querycommem = "SELECT * FROM tblComMemLink"
        self.commem_row = self.cur.execute(self.querycommem).fetchall()
        self.querycom = "SELECT * FROM tblComList"
        self.com_row = self.cur.execute(self.querycom).fetchall()
        self.queryclaimcom = "SELECT * FROM tblClaimComLink"
        self.user_claimcom = self.cur.execute(self.queryclaimcom).fetchall()

        self.col_mem = ['MemID','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Member_No','Comments','MDate','MUser']
        self.df_mem = pd.DataFrame(self.mem_row, columns=self.col_mem).fillna("")
        self.col_commem = ['ComID','MemID','PhaseID','GroupID','HHID','ID','PID','ODH','Relationship','CDate','MDate','CUser','MUser']
        self.df_commem = pd.DataFrame(self.commem_row, columns=self.col_commem).fillna("")
        self.col_com = ['ComID','ComName','ComType','ChairLastName','ChairFirstName','RegNo','ChairIDNo','ChairContactNo','Comments','ChairAddress','ChairDeceased','ChairGender','CDate','MDate','CUser','MUser']
        self.df_com = pd.DataFrame(self.com_row, columns=self.col_com).fillna("")
        self.col_claimcom = ['ComID','ClaimID','ID','CDate','MDate','CUser','MUser']
        self.df_claimcom = pd.DataFrame(self.claimcom_row, columns=self.col_claimcom).fillna("")

        #creating count for recordid
        self.rid_last = self.df_list.values[-1].tolist()[0]
        #self.rid_last +=1

        self.link_last = len(self.df_link.values.tolist())

        #pulling values from dataframe
        self.claimopt = self.df_claim.values.tolist()
        self.listopt = self.df_list.values.tolist()
        self.linkopt = self.df_link.values.tolist()
        self.useropt = self.df_user.values.tolist()
        #convert to dictionary
        self.userdict = self.df_user.set_index('UserLogin').T.to_dict('dict')

        #merging dataframe
        self.df_linklist = pd.merge(self.df_link, self.df_list, how="left", on=["BenID"], indicator=True)
        self.df_linklist.sort_values(by=['ClaimID','BenID','LinkID','Generation'], inplace=True, ascending=False)
        self.linklistopt = self.df_linklist.values.tolist()

        self.df_newlist = pd.merge(self.df_list, self.df_link, how="left", on=["BenID"], indicator=True)
        self.df_newlist.sort_values(by=['BenID'], inplace=True, ascending=False)
        self.newlistopt = self.df_newlist.values.tolist()
        #print(df_newlist.info())


		
