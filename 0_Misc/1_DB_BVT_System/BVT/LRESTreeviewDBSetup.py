from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from collections import defaultdict
import sqlite3
from sqlalchemy import create_engine
import datetime
import csv
import os
import networkx as nx
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


cur.execute(
    """CREATE TABLE IF NOT EXISTS tblFamList (RecordID INTEGER PRIMARY KEY, NoDetail integer, Claimant integer, LastName text, FirstName text, Gender text, 
            IDNo text, DOB text, Deceased integer, Eligible integer, Dispossessed integer, 
            HomeNumber text, CDate text, CUser text, PassportNo text, Nationality text, 
            CellNumber text, WorkNumber text, EmailAddress text, PostalAddress text, 
            PhysicalAddress text,  City text, Province text, Country text, ZipCode text, 
            Married integer, Disabled integer, POA integer, Comments text, MDate text, MUser text)""")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblClaimFamLink (RecordID INTEGER, LinkID integer, ID integer, PID integer, ClaimID integer, Generation text, RelationshipID integer, Relationship text, CDate text, CUser text, MDate text, MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblClaimList (ClaimID INTEGER PRIMARY KEY, ClaimName text, Status text, ClaimFileNumber text, Progress text, ClaimantName text, ClaimantReference text, ProjectName text, Province text, District text, Comment text, EstimatedBudget text, EstimatedOptions integer, LandType text, ClaimType text, Rule5Status text, Rule5ApproveDate text, RegistryNumber text, CDate text, CUser text, MDate text, MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblUserList (UserID INTEGER PRIMARY KEY, Username text, UserLogin text, UserPassword text, UserDepartment text, Address text, City text, Province text, PhoneNumber text, UserSecurity integer)")
conn.commit()


##LOAD DATA FROM CSV##

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

'''
'''
##IMPUTING DATA##

# Adding leading zero to id number and phone number
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


exp_header = ['RecordID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
filename = "{}".format(sd) + "csvFamList.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(exp_header)
    for record in listdata:
        exp_writer.writerow(record)
       

##DELETE UNLINKED RECORDS##

#delete unlinked record
df_newlist = pd.merge(df_list, df_link, how="left", on=["RecordID"], indicator=True)
df_newlist.sort_values(by=['RecordID'], inplace=True, ascending=False)
newlistopt = df_newlist.values.tolist()

newrec = []
lastcol = len(df_newlist.columns)-1
for i in newlistopt:
        if i[lastcol] == "left_only":
            newrec.append(i[0])
            cur.execute("DELETE FROM tblFamList WHERE RecordID=?", (i[0],))
conn.commit()


queryoutlist = "SELECT * FROM tblFamList"
outlist_row = cur.execute(queryoutlist).fetchall()
print(outlist_row)

col_outlist = ['RecordID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
df_outlist = pd.DataFrame(outlist_row, columns=col_outlist).fillna("")

outlistopt = df_outlist.values.tolist()

filename = "{}".format(sd) + "csvFamList.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(col_outlist)
    for record in outlistopt:
        exp_writer.writerow(record)


##CLEAN DATA

# Clean estimated budget value
claimdata = df_claim.values.tolist()
#to_remove = ["R",","," "]
for record in claimdata:
    print(record[11])
    record[11].replace(",",".")
    #for x in to_remove:
        #record[11].replace(x,"")



exp_header = ['ClaimID', 'ClaimName', 'Status', 'ClaimFileNumber', 'Progress', 'ClaimantName', 'ClaimantReference', 'ProjectName', 'Province', 'District', 'Comment', 'EstimatedBudget', 'EstimatedOptions', 'LandType', 'ClaimType', 'Rule5Status', 'Rule5ApproveDate', 'RegistryNumber', 'CDate', 'CUser', 'MDate', 'MUser']
filename = "{}".format(sd) + "csvClaimList_.csv"
with open(filename, mode='w', newline='',  encoding='utf-8') as myfile:
    exp_writer = csv.writer(myfile, delimiter=';')
    exp_writer.writerow(exp_header)
    for record in claimdata:
        exp_writer.writerow(record)
        
##EXPORT COLUMNS FROM LIST TO LINK TABLE

querylist = "SELECT * FROM tblFamList"
list_row = cur.execute(querylist).fetchall()
querylink = "SELECT * FROM tblClaimFamLink"
link_row = cur.execute(querylink).fetchall()


#print(df_claim["EstimatedBudget"].values.tolist())
col_list = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
df_list = pd.DataFrame(list_row, columns=col_list).fillna("")
col_link = ['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser']
df_link = pd.DataFrame(link_row, columns=col_link).fillna("")


#merging dataframe
df_linklist = pd.merge(df_link, df_list, how="left", on=["BenID"], indicator=True)
df_linklist.sort_values(by=['ClaimID','BenID','LinkID','Generation'], inplace=True, ascending=False)

df_linklist_col = df_linklist[['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser','Eligible', Deceased, Dispossessed, Married, Disabled, POA, ]]


df_linklist_col.to_csv("{}".format(sd) + "csvClaimFamLink_stats.csv"", sep=";", encoding='utf-8', index=False)
'''

##AWARD CALCULATION##

queryclaim = "SELECT * FROM tblClaimList"
claim_row = cur.execute(queryclaim).fetchall()
querylist = "SELECT * FROM tblFamList"
list_row = cur.execute(querylist).fetchall()
querylink = "SELECT * FROM tblClaimFamLink"
link_row = cur.execute(querylink).fetchall()


col_claim = ['ClaimID', 'ClaimName', 'Status', 'ClaimFileNumber', 'Progress', 'ClaimantName', 'ClaimantReference', 'ProjectName', 'Province', 'District', 'Comment', 'EstimatedBudget', 'EstimatedOptions', 'LandType', 'ClaimType', 'Rule5Status', 'Rule5ApproveDate', 'RegistryNumber', 'CDate', 'CUser', 'MDate', 'MUser']
df_claim = pd.DataFrame(claim_row, columns=col_claim)
df_claim["EstimatedBudget"].replace('', np.nan, inplace =True)
#df_claim['EstimatedBudget'].astype('float')
df_claim.dropna(subset=["EstimatedBudget"], inplace =True)
#print(list(df_claim["EstimatedBudget"]))

#print(df_claim["EstimatedBudget"].values.tolist())
col_list = ['BenID','NoDetail','Claimant','LastName','FirstName','Gender','IDNo','DOB','Deceased','Eligible','Dispossessed','HomeNumber','CDate','CUser','PassportNo','Nationality','CellNumber','WorkNumber','EmailAddress','PostalAddress','PhysicalAddress','City','Province','Country','ZipCode','Married','Disabled','POA','Comments','MDate','MUser']
df_list = pd.DataFrame(list_row, columns=col_list).fillna("")
col_link = ['BenID','LinkID','ID','PID','ClaimID','Generation','RelationshipID','Relationship','CDate','MDate','CUser','MUser']
df_link = pd.DataFrame(link_row, columns=col_link).fillna("")


#merging dataframe
df_linklist = pd.merge(df_link, df_list, how="left", on=["BenID"], indicator=True)
df_linklist.sort_values(by=['ClaimID','BenID','LinkID','Generation'], inplace=True, ascending=False)


# Calculate the cash award for each beneficiary
#clam_dict = df_claim.set_index('ClaimID').to_dict('index')
claim_lst = df_claim[['ClaimID','EstimatedBudget']].to_records(index=False)
ben_dict = df_linklist.set_index(['ID']).to_dict('index')
#print(ben_dict)

df_node = df_linklist[['ID','PID']]
G_tree = nx.from_pandas_edgelist(df_node, source='PID', target='ID', create_using=nx.DiGraph())
print(G_tree.number_of_nodes()) 
#print(ben_dict['345.1283.467.2'])
#print(list(G_tree.successors('345.1283.467.2')))


#[3]

def descendants(G,s):
    """
    Using networkx to find direct descendents of parent nodes.
    Create dictionary of deceased parents with list of eligible descendents

    """
    e_ben_dict={}
    parent = list([str(s)])
    while(1):
        if len(parent) == 0:
            return e_ben_dict
        e_ben_lst = []
        for each in parent:
            ben_lst = list(G.successors(str(each)))
            tmp_d = []
            for ben in ben_lst:
                # if eligible -> create a list of children for deceased parent
                if ben_dict[ben]["Eligible"] == True:
                    e_ben = (each, ben)
                    e_ben_lst.append(e_ben)
                    # if deceased or odi spouse -> find children
                    if ben_dict[ben]["Deceased"] == True or ben_dict[ben]["RelationshipID"] == 2 :
                        tmp_d.append(ben)
        parent = list(tmp_d)
        for k,v in e_ben_lst:
            e_ben_dict.setdefault(k, []).append(v)


#Calculate share of award for grand descendants
def share_ben(claim,ben,award,share=None):
    """
    Using dictionary of lists to calculate the share of award to eligible beneficiaries.
    Create list of tuples of award share and amount to eligible beneficiaries.

    """
    award_lst = []
    parent_lst = list([(ben,share,award)])
    e_tree = descendants(G_tree,str(claim))
    while(1):
        if len(parent_lst) == 0:
            return award_lst
        d_ben_lst =[]    
        for parent,share,award in parent_lst:
            e_ben_lst = e_tree.get(str(parent),None)
            # if deceased parent has no eligible descendents -> mark as not eligible
            if e_ben_lst is None:
                print("Warning: " + parent + " is eligible and deceased with no eligible descendants!")
                note = "Not Eligible"
                tot_e_ben = (parent,share,award,note)
                award_lst.append(tot_e_ben)
            else:
                tot_e_award = 0
                tot_e_award_lst = []
                tmp=[]
                for e_ben in e_ben_lst:
                    # if eligible -> calculate share
                    if ben_dict[e_ben]['Eligible'] == True:
                        rid = ben_dict[e_ben]['RelationshipID']
                        no_e_ben = len(e_ben_lst)
                        share_e_ben = 1/no_e_ben
                        award_e_ben = award*(1/no_e_ben)

                        # special case: if odi spouse alive and has child -> calculate share 
                        if rid == 2:
                            if ben_dict[e_ben]['Deceased'] == False:
                                child_lst = e_tree.get(str(e_ben),None)
                                if child_lst is not None:
                                    no_child = len(child_lst)
                                    award_spouse = calc_share(claim,e_ben,no_e_ben,award,parent,rid,no_child)
                                    if award_spouse is not None:
                                        for s_s,a_s in award_spouse:
                                            share_e_ben = s_s
                                            award_e_ben = a_s
                                    d_ben = (e_ben,share_e_ben,award_e_ben)
                                    d_ben_lst.append(d_ben)

                        # special case: if child has parent alive -> calculate share 
                        elif rid == 3:
                            if ben_dict[parent]['Deceased'] == False:
                                award_child = calc_share(claim,e_ben,no_e_ben,award,parent,rid)
                                if award_child is not None:
                                    for s_c,a_c in award_child:
                                        share_e_ben = s_c
                                        award_e_ben = a_c
                        # no special case
                        else:
                            pass

                        # if alive -> assign share
                        if ben_dict[e_ben]['Deceased'] == False: 
                            award_e_note = "Eligible"             
                            tot_e_ben = (e_ben,share_e_ben,award_e_ben,award_e_note)
                            tmp.append(tot_e_ben)
                            award_lst.append(tot_e_ben)
                        # if deceased -> find descendents
                        elif ben_dict[e_ben]['Deceased'] == True: 
                            d_ben = (e_ben,share_e_ben,award_e_ben)
                            d_ben_lst.append(d_ben)

        parent_lst  = list(d_ben_lst)



def calc_share(claim,ben,no_ben,award,parent,rid,no_child=None):
    """
    Special case:
    Using dictionary of lists to calculate the share of award to eligible spouse with child.
    Create tuples of award share and amount to eligible spouse with child.

    """
    award_lst = []
    ben_lst = []
    remainder = 0.01
    tmp = []

    if rid == 2:
        print("alive spouse has child")
        # if odi spouse was not present at dispossession -> assign odi spouse 50%
        if ben_dict[ben]['Dispossessed'] == False:
            print("alive spouse not dispossessed")     
            share_spouse = (1/no_ben)*0.5
            award_spouse = award*(1/no_ben)*0.5
            tot_spouse = (share_spouse,award_spouse)

        # if odi spouse was present at dispossession -> assign odi spouse 50% + child share
        elif ben_dict[ben]['Dispossessed'] == True:
            print("alive spouse dispossessed")  
            share_spouse = (1/no_ben)*0.5*(1+(1/(no_child + 1)))
            award_spouse = award*(1/no_ben)*0.5*(1+(1/(no_child + 1)))
            tot_spouse = (share_spouse,award_spouse)
        tmp.append(tot_spouse)

    elif rid == 3:
        # if odi spouse was not present at dispossession -> assign child 50%
        if ben_dict[parent]['Dispossessed'] == False:
            print("alive spouse not dispossessed + child")     
            share_child = (1/no_ben)
            award_child = award*(1/no_ben)
            tot_child = (share_child,award_child)

        # if odi spouse was present at dispossession -> assign child 50% minus odi spouse share
        elif ben_dict[parent]['Dispossessed'] == True:
            print("alive spouse dispossessed + child")  
            share_child = (1/(no_ben + 1))
            award_child = award*(1/(1+(1/(no_ben + 1))))*(1/(no_ben + 1))
            tot_child = (share_child,award_child)
        tmp.append(tot_child)
                
    return tmp


#print(e_tree['235'])
#print(share_ben('235','235',100000.00))

s_tree = {} 
for claim,award in claim_lst:
    if G_tree.has_node(str(claim)): 
        s = share_ben(str(claim),str(claim),float(award))
        s_tree[str(claim)] = s
        print(s_tree)

'''
def calc_remainder()
    s_tree = share_ben(str(claim),str(claim),float(award))
    sorted_ben_dict = {k:v for k,v in sorted(ben_dict.items(), key=lambda item: item["IDNo"])}
    i=1
    while i < len(ben_dict)+1:
    for k,v in sorted_ben_dict:
        sorted_ben_dict[k]['sort'] =  i
        i+=1

    tot_award = sum(w for k,v,w,x in s_tree)
    tot_rem = award - tot_award
    r = 0.01
    while r < tot_rem
        for k,w,v,x in s_tree:
        r +=0.01
  
'''
# Build a directed graph and a list of all names that are odi
#graph = {name: set() for tup in lst for name in tup}



'''
##OUTPUT TABLES##

cur.execute("SELECT * FROM tblClaimList")
records1 = cur.fetchall()
print(records1)


cur.execute("SELECT * FROM tblClaimFamLink")
records2 = cur.fetchall()
print(records2)


cur.execute("SELECT rowid, * FROM tblFamList")
records3 = cur.fetchall()
print(records3)


cur.execute("SELECT rowid, * FROM tblUserList")
records4 = cur.fetchall()
print(records4)


querylistlink = "SELECT tblFamList.RecordID, tblClaimFamLink.LinkID, tblFamList.FirstName, tblFamList.LastName, tblClaimFamLink.Relationship, tblFamList.Claimant, \
        tblClaimFamLink.ID, tblClaimFamLink.PID, tblClaimFamLink.ClaimID, tblFamList.FirstName & ' ' & tblFamList.LastName & IIF(tblFamList.Deceased = True, ' (D)', '') AS RecordName, tblClaimFamLink.Generation, tblClaimFamLink.RelationshipID, tblFamList.Deceased \
        FROM tblClaimList INNER JOIN (tblClaimFamLink LEFT JOIN tblFamList ON tblClaimFamLink.RecordID = tblFamList.RecordID) ON tblClaimList.ClaimID = tblClaimFamLink.ClaimID \
        WHERE tblClaimFamLink.ClaimID = 1 \
        ORDER BY tblClaimFamLink.Generation, tblFamList.RecordID"
cur.execute(querylistlink)
linkchildrows = cur.fetchall()
print(linkchildrows)

'''
conn.close()