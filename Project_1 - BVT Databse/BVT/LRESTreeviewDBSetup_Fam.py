from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import datetime
import csv
import os
#import xlrd

#\\researchdata.uct.ac.za\LRES\Survey_Assistants\LRES_Database\PyDatabase
sd = '//researchdata.uct.ac.za/LRES/Survey_Assistants/LRES_Database/PyDatabase/'
##SETUP DATABASE##
conn = sqlite3.connect("{}".format(sd) + "lres_tree.db")
cur = conn.cursor()

'''
cur.execute(
    "DROP TABLE IF EXISTS tblFamList")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblClaimFamLink")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblClaimList")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblUserList")
conn.commit()
'''

cur.execute(
    """CREATE TABLE IF NOT EXISTS tblFamList (BenID INTEGER, NoDetail integer, Claimant integer, LastName text, FirstName text, Gender text, 
            IDNo text, DOB text, Deceased integer, Eligible integer, Dispossessed integer, 
            HomeNumber text, CDate text, CUser text, PassportNo text, Nationality text, 
            CellNumber text, WorkNumber text, EmailAddress text, PostalAddress text, 
            PhysicalAddress text,  City text, Province text, Country text, ZipCode text, 
            Married integer, Disabled integer, POA integer, Comments text, MDate text, MUser text)""")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblClaimFamLink (BenID INTEGER, LinkID integer, ID integer, PID integer, ClaimID integer, Generation text, RelationshipID integer, Relationship text, CDate text, CUser text, MDate text, MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblClaimList (ClaimID INTEGER, ClaimName text, Status text, ClaimFileNumber text, Progress text, ClaimantName text, ClaimantReference text, ProjectName text, Province text, District text, Comment text, EstimatedBudget text, EstimatedOptions text, LandType text, ClaimType text, Rule5Status text, Rule5ApproveDate text, RegistryNumber text, CDate text, CUser text, MDate text, MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblUserList (UserID INTEGER , Username text, UserLogin text, UserPassword text, UserDepartment text, Address text, City text, Province text, PhoneNumber text, UserSecurity integer)")
conn.commit()

'''

dfc = pd.read_csv("{}".format(sd) + "csvClaimList.csv", sep=";")
df_claim = dfc.fillna("")
dfls = pd.read_csv("{}".format(sd) + "csvFamList.csv", sep=";", dtype={'IDNo': str, 'HomeNumber': str, 'CellNumber': str, 'WorkNumber': str})
df_list = dfls.fillna("")
dflk = pd.read_csv("{}".format(sd) + "csvClaimFamLink.csv", sep=";", dtype={'LinkID': str})
df_link = dflk.fillna("")
dfu = pd.read_csv("{}".format(sd) + "csvUserList.csv", sep=";")
df_user = dfu.fillna("")

df_claim.to_sql('tblClaimList', conn, if_exists='replace', index=False, chunksize=10000)
df_link.to_sql('tblClaimFamLink', conn, if_exists='replace', index=False, chunksize=10000)
df_list.to_sql('tblFamList', conn, if_exists='replace', index=False, chunksize=10000)
df_user.to_sql('tblUserList', conn, if_exists='replace', index=False, chunksize=10000)


##SETUP TEMPORARY DATABASE##
#infile = infile
#claimsheet = claimsheet
#listsheet = listsheet
#linksheet = linksheet
#usersheet = usersheet
engine = create_engine(db, echo=False)
conn =  engine.connect()

#TRANSFORM DATA EXCEL <-> SQL <-> PYTHON 
#pulls data from excel, creates sql database, analyse in python then destroy database and push back to excel


#pull excel data
dfc = pd.read_excel(infile, sheet_name=claimsheet)
df_claim = dfc.fillna("")
dfls = pd.read_excel(infile, sheet_name=listsheet, dtype={'IDNo': str, 'HomeNumber': str})
#dfls['DOB'] = pd.to_datetime(dfls['DOB'], format='%Y%m%d', errors='coerce')
df_list = dfls.fillna("")
dflk = pd.read_excel(infile, sheet_name=linksheet, dtype={'LinkID': str})
df_link = dflk.fillna("")
dfu = pd.read_excel(infile, sheet_name=usersheet)
df_user = dfu.fillna("")

#specify temporary database table 
df_claim.to_sql('tblClaimList', engine, if_exists='replace', index=False)
df_link.to_sql('tblClaimFamLink', engine, if_exists='replace', index=False)
df_list.to_sql('tblFamList', engine, if_exists='replace', index=False)
df_user.to_sql('tblUser', engine, if_exists='replace', index=False)



listdata = df_list.values.tolist()
for record in listdata:

    if len(record[6]) == 10:
        record[6] = "000"+ str(record[6])

    if len(record[6]) == 11:
        record[6] = "00"+ str(record[6])

    if len(record[6]) == 12:
        record[6]= "0" + str(record[6])

    if len(record[11]) == 9:
        record[11] = "0"+ str(record[11])

    if len(record[16]) == 9:
        record[16] = "0"+ str(record[16])

    if len(record[17]) == 9:
        record[17] = "0"+ str(record[17])


exp_header = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
filename = "{}".format(sd) + "csvFamList.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(exp_header)
    for record in listdata:
        exp_writer.writerow(record)
       

#delete unlinked record
df_newlist = pd.merge(df_list, df_link, how="left", on=["BenID"], indicator=True)
df_newlist.sort_values(by=['BenID'], inplace=True, ascending=False)
print(df_newlist)
newlistopt = df_newlist.values.tolist()

newrec = []
lastcol = len(df_newlist.columns)-1
for i in newlistopt:
        if i[lastcol] == "left_only":
            newrec.append(i[0])
            cur.execute("DELETE FROM tblFamList WHERE BenID=?", (i[0],))
print(len(newrec)) 
conn.commit()


queryoutlist = "SELECT * FROM tblFamList"
outlist_row = cur.execute(queryoutlist).fetchall()
#print(outlist_row)

col_outlist = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
df_outlist = pd.DataFrame(outlist_row, columns=col_outlist).fillna("")

outlistopt = df_outlist.values.tolist()

filename = "{}".format(sd) + "csvFamListx.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(col_outlist)
    for record in outlistopt:
        exp_writer.writerow(record)



cur.execute("SELECT * FROM tblClaimList")
records1 = cur.fetchall()
print(records1)


cur.execute("SELECT * FROM tblClaimFamLink")
records2 = cur.fetchall()
print(records2)

'''
cur.execute("SELECT rowid, * FROM tblFamList")
records3 = cur.fetchall()
print(records3)
print(len(records3)) #12561
'''

cur.execute("SELECT rowid, * FROM tblUserList")
records4 = cur.fetchall()
print(records4)


querylistlink = "SELECT tblFamList.BenID, tblClaimFamLink.LinkID, tblFamList.FirstName, tblFamList.LastName, tblClaimFamLink.Relationship, tblFamList.Claimant, \
        tblClaimFamLink.ID, tblClaimFamLink.PID, tblClaimFamLink.ClaimID, tblFamList.FirstName & ' ' & tblFamList.LastName & IIF(tblFamList.Deceased = True, ' (D)', '') AS BenName, tblClaimFamLink.Generation, tblClaimFamLink.RelationshipID, tblFamList.Deceased \
        FROM tblClaimList INNER JOIN (tblClaimFamLink LEFT JOIN tblFamList ON tblClaimFamLink.BenID = tblFamList.BenID) ON tblClaimList.ClaimID = tblClaimFamLink.ClaimID \
        WHERE tblClaimFamLink.ClaimID = 1 \
        ORDER BY tblClaimFamLink.Generation, tblFamList.BenID"
cur.execute(querylistlink)
linkchildrows = cur.fetchall()
print(linkchildrows)

'''
conn.close()