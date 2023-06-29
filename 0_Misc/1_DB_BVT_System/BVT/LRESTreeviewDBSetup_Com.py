from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
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


cur.execute(
    "DROP TABLE IF EXISTS tblMemList")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblComMemLink")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblComList")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblClaimComLink")
conn.commit()


cur.execute(
    """CREATE TABLE IF NOT EXISTS tblMemList (MemID INTEGER PRIMARY KEY, Claimant integer, LastName text, FirstName text, Gender text, 
            IDNo text, DOB text, Deceased integer, Eligible integer, HomeNumber text, 
            CDate text, CUser text, PassportNo text, Nationality text, CellNumber text, WorkNumber text, 
            EmailAddress text, PostalAddress text, PhysicalAddress text,  City text, Province text, 
            Country text, ZipCode text, Married integer, Disabled integer, POA integer, Comments text, 
            Member_No text, MDate text, MUser text)""")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblComMemLink (ComID integer,MemID integer,PhaseID integer,GroupID integer,HHID integer,ID integer, PID integer, ODH text,Relationship text,CDate text,MDate text,CUser text,MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblComList (ComID INTEGER PRIMARY KEY,ComName text,ComType text,ChairLastName text,ChairFirstName text,RegNo text,ChairIDNo text,ChairContactNo text,Comments text,ChairAddress text,ChairDeceased integer,ChairGender text,CDate text,MDate text,CUser text,MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblClaimComLink (ComID integer, ClaimID integer, ID integer, CDate text, MDate text, CUser text, MUser text)")
conn.commit()



dfcom = pd.read_csv("{}".format(sd) + "csvComList.csv", sep=";", dtype={'ChairIDNo': str, 'ChairContactNo': str})
df_com = dfcom.fillna("")
dfmem = pd.read_csv("{}".format(sd) + "csvMemList.csv", sep=";", dtype={'IDNo': str, 'HomeNumber': str, 'CellNumber': str, 'WorkNumber': str})
df_mem = dfmem.fillna("")
dfcommem = pd.read_csv("{}".format(sd) + "csvComMemLink.csv", sep=";")

dfcommem["IDx"] = dfcommem["ComID"].map(str) + "." + dfcommem["MemID"].map(str) + "." + dfcommem["PhaseID"].map(str) + "." + dfcommem["GroupID"].map(str)
#dfcommem["PIDx"] = dfcommem.loc[dfcommem["HHID"] != np.nan, '"PIDx"'
dfcommem["PIDx"] = dfcommem["HHID"].apply(lambda x: dfcommem["ComID"].map(str) \
    + "." + dfcommem["MemID"].map(str) + "." + dfcommem["PhaseID"].map(str) \
    + "." + dfcommem["GroupID"].map(str) if x != np.nan else dfcommem["DispID"])
col_commem = ['ComID','MemID','PhaseID','GroupID','HHID','IDx','ID','PIDx','PID','ODH','Relationship','CDate','MDate','CUser','MUser']
dfcommem = dfcommem.reindex(columns=col_commem)
df_commem = dfcommem.fillna("")
dfclmcom = pd.read_csv("{}".format(sd) + "csvClaimComLink.csv", sep=";")
df_clmcom = dfclmcom.fillna("")


df_mem.to_sql('tblMemList', conn, if_exists='replace', index=False, chunksize=10000)
df_commem.to_sql('tblComMemLink', conn, if_exists='replace', index=False, chunksize=10000)
df_com.to_sql('tblComList', conn, if_exists='replace', index=False, chunksize=10000)
df_clmcom.to_sql('tblClaimComLink', conn, if_exists='replace', index=False, chunksize=10000)



'''
#comedit
comdata = df_com.values.tolist()
for record in comdata:

    if len(record[6]) == 10:
        record[6] = "000"+ str(record[6])

    if len(record[6]) == 11:
        record[6] = "00"+ str(record[6])

    if len(record[6]) == 12:
        record[6]= "0" + str(record[6])

    if len(record[7]) == 9:
        record[7] = "0"+ str(record[7])



exp_header = ['ComID','ComName','ComType','ChairLastName','ChairFirstName','RegNo','ChairIDNo','ChairContactNo','Comments','ChairAddress','ChairDeceased','ChairGender','CDate','MDate','CUser','MUser']
filename = "{}".format(sd) + "csvComList.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(exp_header)
    for record in comdata:
        exp_writer.writerow(record)


#memedit
memdata = df_mem.values.tolist()
for record in memdata:

    if len(record[5]) == 10:
        record[5] = "000"+ str(record[5])

    if len(record[5]) == 11:
        record[5] = "00"+ str(record[5])

    if len(record[5]) == 12:
        record[5]= "0" + str(record[5])

    if len(record[9]) == 9:
        record[9] = "0"+ str(record[9])

    if len(record[14]) == 9:
        record[14] = "0"+ str(record[14])

    if len(record[15]) == 9:
        record[15] = "0"+ str(record[15])


exp_header = ['MemID','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','Member_No','MDate','MUser']
filename = "{}".format(sd) + "csvMemList.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(exp_header)
    for record in memdata:
        exp_writer.writerow(record)
 


##UNLINKED MEM
#delete unlinked record
df_newlist = pd.merge(df_mem, df_commem, how="left", on=["MemID"], indicator=True)
df_newlist.sort_values(by=['MemID'], inplace=True, ascending=False)
#print(df_newlist)
newlistopt = df_newlist.values.tolist()

newrec = []
lastcol = len(df_newlist.columns)-1
for i in newlistopt:
        if i[lastcol] == "left_only":
            newrec.append(i[0])
            cur.execute("DELETE FROM tblMemList WHERE MemID=?", (i[0],))
print(len(newrec)) #260
conn.commit()

queryoutlist = "SELECT * FROM tblMemList"
outlist_row = cur.execute(queryoutlist).fetchall()
#print(outlist_row)

col_outlist = ['MemID','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Member_No','Comments','MDate','MUser']
df_outlist = pd.DataFrame(outlist_row, columns=col_outlist).fillna("")
outlistopt = df_outlist.values.tolist()

filename = "{}".format(sd) + "csvMemListx.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(col_outlist)
    for record in outlistopt:
        exp_writer.writerow(record)



cur.execute("SELECT * FROM tblComList")
records1 = cur.fetchall()
print(records1)


cur.execute("SELECT * FROM tblClaimComLink")
records2 = cur.fetchall()
print(records2)


cur.execute("SELECT * FROM tblMemList")
records3 = cur.fetchall()
print(records3)
print(len(records3)) #18039

'''
cur.execute("SELECT * FROM tblComMemLink")
records4 = cur.fetchall()
print(records4)
'''

querylistlink = "SELECT tblMemList.MemID, tblComMemLink.HHID, tblMemList.FirstName, tblMemList.LastName, tblComMemLink.Relationship, tblMemList.Claimant, \
        tblComMemLink.ID, tblComMemLink.PID, tblComMemLink.ComID, tblMemList.FirstName & ' ' & tblMemList.LastName & IIF(tblMemList.Deceased = 1, ' (D)', '') AS MemName, \
        tblComMemLink.ODH, tblComMemLink.PhaseID, tblComMemLink.GroupID, tblMemList.Deceased, tblComList.ComName, tblComList.ComType, tblClaimComLink.ClaimID \
        FROM (tblComList LEFT JOIN (tblComMemLink LEFT JOIN tblMemList ON tblComMemLink.MemID = tblMemList.MemID) ON tblComList.ComID = tblComMemLink.ComID) \
        INNER JOIN (tblClaimList LEFT JOIN tblClaimComLink ON tblClaimList.ClaimID = tblClaimComLink.ClaimID) ON tblComList.ComID = tblClaimComLink.ComID \
        ORDER BY tblComMemLink.PhaseID, tblComMemLink.GroupID, tblMemList.MemID"
cur.execute(querylistlink)
linkchildrows = cur.fetchall()
print(linkchildrows)
'''

conn.close()