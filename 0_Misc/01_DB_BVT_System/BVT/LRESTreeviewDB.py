from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
from collections import defaultdict
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

class Database:
    #def __init__(self, infile, claimsheet, listsheet, linksheet, usersheet, db):
    def __init__(self, db):
        #\\researchdata.uct.ac.za\LRES\Survey_Assistants\LRES_Database\PyDatabase
        
        ##SETUP DATABASE##
        #print(resource_path(db))
        #self.conn = sqlite3.connect(resource_path(db))
        self.conn = sqlite3.connect("{}".format(sd) + db)

        self.cur = self.conn.cursor()

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tblFamList (BenID INTEGER PRIMARY KEY, NoDetail integer, Claimant integer, LastName text, FirstName text, Gender text, 
                    IDNo text, DOB text, Deceased integer, Eligible integer, Dispossessed integer, 
                    HomeNumber text, CDate text, CUser text, PassportNo text, Nationality text, 
                    CellNumber text, WorkNumber text, EmailAddress text, PostalAddress text, 
                    PhysicalAddress text,  City text, Province text, Country text, ZipCode text, 
                    Married integer, Disabled integer, POA integer, Comments text, MDate text, MUser text)""")
        self.conn.commit()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tblClaimFamLink (BenID integer, LinkID integer, ID integer, PID integer, ClaimID integer, Generation text, RelationshipID integer, Relationship text, CDate text, CUser text, MDate text, MUser text, Award text)")
        self.conn.commit()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tblClaimList (ClaimID INTEGER PRIMARY KEY, ClaimName text, Status text, ClaimFileNumber text, Progress text, ClaimantName text, ClaimantReference text, ProjectName text, Province text, District text, Comment text, EstimatedBudget text, EstimatedOptions text, LandType text, ClaimType text, Rule5Status text, Rule5ApproveDate text, RegistryNumber text, CDate text, CUser text, MDate text, MUser text)")
        self.conn.commit()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tblUserList (UserID INTEGER PRIMARY KEY, Username text, UserLogin text, UserPassword text, UserDepartment text, Address text, City text, Province text, PhoneNumber text, UserSecurity integer)")
        self.conn.commit()


        self.queryclaim = "SELECT * FROM tblClaimList"
        self.claim_row = self.cur.execute(self.queryclaim).fetchall()
        self.querylink = "SELECT * FROM tblClaimFamLink"
        self.link_row = self.cur.execute(self.querylink).fetchall()
        self.querylist = "SELECT * FROM tblFamList"
        self.list_row = self.cur.execute(self.querylist).fetchall()
        self.queryuser = "SELECT * FROM tblUserList"
        self.user_row = self.cur.execute(self.queryuser).fetchall()

        self.col_claim = ['ClaimID', 'ClaimName', 'Status', 'ClaimFileNumber', 'Progress', 'ClaimantName', 'ClaimantReference', 'ProjectName', 'Province', 'District', 'Comment', 'EstimatedBudget', 'EstimatedOptions', 'LandType', 'ClaimType', 'Rule5Status', 'Rule5ApproveDate', 'RegistryNumber', 'CDate', 'CUser', 'MDate', 'MUser']
        self.df_claim = pd.DataFrame(self.claim_row, columns=self.col_claim).fillna("")
        self.col_list = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
        self.df_list = pd.DataFrame(self.list_row, columns=self.col_list).fillna("")
        self.col_link = ['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser']
        self.df_link = pd.DataFrame(self.link_row, columns=self.col_link).fillna("")
        self.col_user = ['UserID','Username','UserLogin','UserPassword','UserDepartment','Address','City','Province','PhoneNumber','UserSecurity']
        self.df_user = pd.DataFrame(self.user_row, columns=self.col_user).fillna("")
    
        #creating count for recordid
        #self.rid_last = self.df_list.values[-1].tolist()[0]
        #self.rid_last = 20000
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

        self.df_claimlinklist = pd.merge(self.df_claim, self.df_linklist, how="left", on=["ClaimID"], indicator=True)
        self.df_claimlinklist.sort_values(by=['ClaimID','BenID','LinkID','Generation'], inplace=True, ascending=False)
        self.claimlinklistopt = self.df_claimlinklist.values.tolist()


    def fetchclaim(self):
        self.queryclaim = "SELECT * FROM tblClaimList"
        self.cur.execute(self.queryclaim)
        claimrows = self.cur.fetchall()
        return claimrows

    def fetchlist(self):
        self.querylist = "SELECT * FROM tblFamList"
        self.cur.execute(self.querylist)
        listrows = self.cur.fetchall()
        return listrows

    def fetchlink(self):
        self.querylink = "SELECT * FROM tblClaimFamLink"
        self.cur.execute(self.querylink)
        linkrows = self.cur.fetchall()
        return linkrows

    def fetchuser(self):
        self.queryuser = "SELECT * FROM tblUserList"
        self.cur.execute(self.queryuser)
        userrows = self.cur.fetchall()
        return userrows

    def fetchlistlink(self):
       	self.querylistlink = "SELECT tblFamList.BenID, tblClaimFamLink.LinkID, tblFamList.FirstName, tblFamList.LastName, tblClaimFamLink.Relationship, tblFamList.Claimant, \
				tblClaimFamLink.ID, tblClaimFamLink.PID, tblClaimFamLink.ClaimID, tblFamList.FirstName & ' ' & tblFamList.LastName & IIF(tblFamList.Deceased = True, ' (D)', '') AS RecordName, \
                tblClaimFamLink.Generation, tblClaimFamLink.RelationshipID, tblFamList.Deceased, tblFamList.Eligible, tblClaimList.EstimatedBudget\
				FROM tblClaimList INNER JOIN (tblClaimFamLink LEFT JOIN tblFamList ON tblClaimFamLink.BenID = tblFamList.BenID) ON tblClaimList.ClaimID = tblClaimFamLink.ClaimID \
				ORDER BY tblClaimFamLink.Generation, tblFamList.BenID"
        self.cur.execute(self.querylistlink)
        linkchildrows = self.cur.fetchall()
        return linkchildrows

    def fetchstate(self, ClaimID):
        self.cur.execute("SELECT tblClaimList.Status, tblClaimList.Progress FROM tblClaimList WHERE tblClaimList.ClaimID = ?", 
            (ClaimID,))
        compstate = self.cur.fetchall()
        return compstate

    def fetchid(self, BenID):
        self.cur.execute("SELECT DISTINCT tblClaimFamLink.BenID FROM tblClaimFamLink WHERE tblClaimFamLink.LinkID = ?",
            (str(BenID),))
        idrows = self.cur.fetchall()
        return idrows

    def filterclaim(self, ClaimID):
        self.cur.execute("SELECT tblClaimList.ClaimID, tblClaimList.ClaimName, tblClaimList.Status, tblClaimList.ClaimFileNumber FROM tblClaimList WHERE tblClaimList.ClaimID = ?", 
            (ClaimID,))
        linkrows = self.cur.fetchall()
        return linkrows

    def filterlist(self, BenID):
        self.cur.execute("SELECT * FROM tblFamList WHERE tblFamList.BenID = ?", 
            (BenID,))
        listrows = self.cur.fetchall()
        return listrows

    def filterlink(self, ClaimID):
        self.cur.execute("SELECT tblFamList.BenID, tblClaimFamLink.LinkID, tblFamList.FirstName, tblFamList.LastName, tblClaimFamLink.Relationship, tblFamList.Claimant, tblClaimFamLink.ID, \
            tblClaimFamLink.PID, tblClaimFamLink.ClaimID, tblFamList.FirstName & ' ' & tblFamList.LastName & IIF(tblFamList.Deceased = True, ' (D)', '') AS RecordName, tblClaimFamLink.Generation, tblClaimFamLink.RelationshipID, tblFamList.Deceased \
            FROM tblClaimList INNER JOIN (tblClaimFamLink LEFT JOIN tblFamList ON tblClaimFamLink.BenID = tblFamList.BenID) ON tblClaimList.ClaimID = tblClaimFamLink.ClaimID \
            WHERE tblClaimFamLink.ClaimID = ? ORDER BY tblClaimFamLink.Generation, tblFamList.BenID", 
            (ClaimID,))
        linkchildrows = self.cur.fetchall()
        return linkchildrows


    def insertclaim(self,ClaimID,ClaimName,Status,ClaimFileNumber,Progress,ClaimantName,ClaimantReference,ProjectName,Province,District,Comment,EstimatedBudget,EstimatedOptions,LandType,ClaimType,Rule5Status,Rule5ApproveDate,RegistryNumber,CDate,CUser,MDate=None,MUser=None):
        self.cur.execute("INSERT INTO tblClaimList  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ClaimID,ClaimName,Status,ClaimFileNumber,Progress,ClaimantName,ClaimantReference,ProjectName,Province,District,Comment,EstimatedBudget,EstimatedOptions,LandType,ClaimType,Rule5Status,Rule5ApproveDate,RegistryNumber,CDate,CUser,MDate,MUser))
        self.conn.commit()
 

    def insertlist(self, BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
			    	IDNo, DOB, Deceased, Eligible, Dispossessed, 
			    	HomeNumber, CDate, CUser, PassportNo=None, Nationality=None, 
			    	CellNumber=None, WorkNumber=None, EmailAddress=None, PostalAddress=None, 
			    	PhysicalAddress=None,  City=None, Province=None, Country=None, ZipCode=None, 
			    	Married=None, Disabled=None, POA=None, Comments=None, MDate=None, MUser=None):
        self.cur.execute("INSERT INTO tblFamList VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, Dispossessed, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments, MDate, MUser))
        self.conn.commit()

    def insertlink(self, BenID, LinkID, ID, PID, ClaimID, Generation, RelationshipID, Relationship, CDate, CUser, MDate=None, MUser=None):
        self.cur.execute("INSERT INTO tblClaimFamLink  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (BenID, LinkID, ID, PID, ClaimID, Generation, RelationshipID, Relationship, CDate, CUser, MDate, MUser))
        self.conn.commit()


    def updatelist(self, BenID, NoDetail, Claimant, LastName, FirstName, Gender, 
                    IDNo, DOB, Deceased, Eligible, Dispossessed, 
                    HomeNumber, CDate, CUser, PassportNo=None, Nationality=None, 
                    CellNumber=None, WorkNumber=None, EmailAddress=None, PostalAddress=None, 
                    PhysicalAddress=None,  City=None, Province=None, Country=None, ZipCode=None, 
                    Married=None, Disabled=None, POA=None, Comments=None, MDate=None, MUser=None):
        self.cur.execute("UPDATE tblFamList SET NoDetail=?, Claimant=?, LastName=?, FirstName=?, Gender=?, \
            IDNo=?, DOB=?, Deceased=?, Eligible=?, Dispossessed=?, HomeNumber=?, CDate=?, CUser=?, PassportNo=?, \
            Nationality=?, CellNumber=?, WorkNumber=?, EmailAddress=?, PostalAddress=?, PhysicalAddress=?,  City=?, \
            Province=?, Country=?, ZipCode=?, Married=?, Disabled=?, POA=?, Comments=?, MDate=?, MUser=? \
            WHERE BenID=?",
            (NoDetail, Claimant, LastName, FirstName, Gender, 
                IDNo, DOB, Deceased, Eligible, Dispossessed, HomeNumber, 
                CDate, CUser, PassportNo, Nationality, CellNumber, WorkNumber, 
                EmailAddress, PostalAddress, PhysicalAddress,
                City, Province, Country, ZipCode, Married, Disabled, 
                POA, Comments, MDate, MUser, BenID))
        self.conn.commit()


    def updateuser(self, UserPassword, UserLogin):
        self.cur.execute("UPDATE tblUserList SET UserPassword = ? WHERE UserLogin = ?",
            (UserPassword, UserLogin))
        self.conn.commit()

    def updatestatus(self, Status, ClaimID):
        self.cur.execute("UPDATE tblClaimlist SET Status = ? WHERE ClaimID = ?",
            (Status, ClaimID))
        self.conn.commit()

    def updateprogress(self, Complete, ClaimID):
        self.cur.execute("UPDATE tblClaimlist SET Progress = ? WHERE ClaimID = ?",
            (Complete, ClaimID))
        self.conn.commit()

    def updateaward(self, Award, ID):
        self.cur.execute("UPDATE tblFamlist SET Award = ? WHERE ID = ?",
            (Award, ID))
        self.conn.commit()


    def removelist(self, BenID):
        self.cur.execute("DELETE FROM tblFamList WHERE BenID=?", 
            (BenID,))
        self.conn.commit()

    def removelink(self, ID):
        self.cur.execute("DELETE FROM tblClaimFamLink WHERE ID=?", 
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
        self.queryclaim = "SELECT * FROM tblClaimList"
        self.claim_row = self.cur.execute(self.queryclaim).fetchall()
        self.querylink = "SELECT * FROM tblClaimFamLink"
        self.link_row = self.cur.execute(self.querylink).fetchall()
        self.querylist = "SELECT * FROM tblFamList"
        self.list_row = self.cur.execute(self.querylist).fetchall()
        self.queryuser = "SELECT * FROM tblUserList"
        self.user_row = self.cur.execute(self.queryuser).fetchall()

        self.col_claim = ['ClaimID', 'ClaimName', 'Status', 'ClaimFileNumber', 'Progress', 'ClaimantName', 'ClaimantReference', 'ProjectName', 'Province', 'District', 'Comment', 'EstimatedBudget', 'EstimatedOptions', 'LandType', 'ClaimType', 'Rule5Status', 'Rule5ApproveDate', 'RegistryNumber', 'CDate', 'CUser', 'MDate', 'MUser']
        self.df_claim = pd.DataFrame(self.claim_row, columns=self.col_claim).fillna("")
        self.col_list = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
        self.df_list = pd.DataFrame(self.list_row, columns=self.col_list).fillna("")
        self.col_link = ['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser']
        self.df_link = pd.DataFrame(self.link_row, columns=self.col_link).fillna("")
        self.col_user = ['UserID','Username','UserLogin','UserPassword','UserDepartment','Address','City','Province','PhoneNumber','UserSecurity']
        self.df_user = pd.DataFrame(self.user_row, columns=self.col_user).fillna("")
    
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

    ##########################################################
     



	    '''
	    graph = defaultdict(set)
	    for child,parent in df_tree[['ID','PID']].values:
	        graph[parent].add(child)

	    #identify root nodes
	    roots = []
	    for node in graph.keys()
	    #if all(node not in children for children in graph.values()):
	    if all(node for node in graph.values().split(".")[-1]==1)
	        roots.append(node)

	    #find the descendents of each root node
	    result = {}
	    for root in roots:
	        visited = set()
	        unvisited = graph[root]
	        while unvisited:
	            visited != unvisited
	            unvisited = set.union(*(graph[node] for nofr in unvisited)) - unvisited
	        result[root] = visited

	    print(result)





    
    def fetchodi(self):
        self.querylistlink = "SELECT tblFamList.BenID, tblClaimFamLink.LinkID, tblFamList.FirstName, tblFamList.LastName, tblClaimFamLink.Relationship, tblFamList.Claimant, \
                tblClaimFamLink.ID, tblClaimFamLink.PID, tblClaimFamLink.ClaimID, tblFamList.FirstName & ' ' & tblFamList.LastName & IIF(tblFamList.Deceased = True, ' (D)', '') AS RecordName, tblClaimFamLink.Generation, tblClaimFamLink.RelationshipID, tblFamList.Deceased,  \
                FROM tblClaimList INNER JOIN (tblClaimFamLink LEFT JOIN tblFamList ON tblClaimFamLink.BenID = tblFamList.BenID) ON tblClaimList.ClaimID = tblClaimFamLink.ClaimID \
                ORDER BY tblClaimFamLink.Generation, tblFamList.BenID"
        self.cur.execute(self.querylistlink)
        linkchildrows = self.cur.fetchall()
        return linkchildrows


    def filterben(self, RelationshipID):
        self.cur.execute("SELECT tblFamList.BenID, tblClaimFamLink.LinkID, tblFamList.FirstName, tblFamList.LastName, tblClaimFamLink.Relationship, tblFamList.Claimant, tblClaimFamLink.ID, \
            tblClaimFamLink.PID, tblClaimFamLink.ClaimID, tblFamList.FirstName & ' ' & tblFamList.LastName & IIF(tblFamList.Deceased = True, ' (D)', '') AS RecordName, \
            tblClaimFamLink.Generation, tblClaimFamLink.RelationshipID, tblFamList.Deceased, tblFamList.Eligible \
            FROM tblClaimList INNER JOIN (tblClaimFamLink LEFT JOIN tblFamList ON tblClaimFamLink.BenID = tblFamList.BenID) ON tblClaimList.ClaimID = tblClaimFamLink.ClaimID \
            WHERE tblClaimFamLink.RelationshipID = ? ORDER BY tblClaimFamLink.Generation, tblFamList.BenID", 
            (RelationshipID,))
        linkchildrows = self.cur.fetchall()
        return linkchildrows

    '''



		
