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


cur.execute(
    "DROP TABLE IF EXISTS tblLandList")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblDisLandLink")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblDisList")
conn.commit()

cur.execute(
    "DROP TABLE IF EXISTS tblClaimDisLink")
conn.commit()


cur.execute(
    """CREATE TABLE IF NOT EXISTS tblLandList (LandID INTEGER PRIMARY KEY, LandType text, FarmErfNumber text, PortionNumber text, FarmTownshipName text, 
            Extent text, LocalAuthority text, RegDivision text, Province text, DistrictMunicipality text, 
            PreviousDescription text, LPICode text, Hectares integer, SquareMeters integer, CurrentLandUse text, TitleDeedNumber text, 
            PropertyOwnerType text, OwnerName text, IdentityNo text, OwnerTelNumber text, OwnerCellNumber text, 
            MultipleOwners integer, MultipleProperties integer, Comments text, LotNumber text, Unregistered integer, DispossessedLand integer, 
            AlternativeLand integer, Latitude text, SubNumber text, LandUse text, Extent_Measure text, ClaimLand_Status text,
            LocationStatus text, LocationStatus_Comment text, Longitude text, CDate text, MDate text, CUser text, MUser text)""")

conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblDisLandLink (LandID integer,DispID integer,PhaseID integer,LandValue text,Improvements text,NegotiatedPrice text,PresentYear text,MVPresentYear text,ValuationOption text,ValuationType text,CDate text,MDate text,CUser text,MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblDisList (DispID INTEGER PRIMARY KEY,PropertyType text,PropertySummary text,MainPlaceName text,DistrictMunicipality text,LocalMunicipality text,Province text ,PropertySize text,Hectares integer,SquareMeters integer,RegisteredRight integer,AuthorityDispossession text,LawDispossession text,LandUseDispossession text,CompensationDispossessionYN integer,CompensationDispossession text,CompensationShortfallAmount text,YearDispossession text,HistoricalValueperUnit text,BaseYear text,CPI_BaseYear text,CPI_DispossessedYear text,MarketValueatDispossession text,TitleDeedNumberDispossession text,HousingQuantum text,FinancialCompensation integer ,LandRestoration integer,SSO text,SSOHousingQuantum text,SSOQuantityHH integer,Comments text,NatureofRight text,Compensation_Status text,Registered_Status text,Extent_Measure text,CDate text,MDate text,CUser text,MUser text)")
conn.commit()

cur.execute(
    "CREATE TABLE IF NOT EXISTS tblClaimDisLink (DispID integer,ClaimID integer,ValuationOption text,ValuationType text,PresentYear text,CPIPresentYear text,CPIDispossessedYear text,MVDispossessedYear text,MVPresentYear text,SSO text,SSOHousingQuantum text,SSONoHH integer,CDate text,MDate text,Cuser text,Muser text)")
conn.commit()



dfland = pd.read_csv("{}".format(sd) + "csvLandList.csv", sep=";", dtype={'FarmErfNumber': str, 'PortionNumber': str, 'LPICode': str, 'IdentityNo':str, 'OwnerTelNumber': str, 'OwnerCellNumber': str, 'Latitude': str, 'Longitude': str})
df_land = dfland.fillna("")
dfdisland = pd.read_csv("{}".format(sd) + "csvDisLandLink.csv", sep=";", dtype={'PhaseID': str, 'PresentYear': str})
df_disland = dfdisland.fillna("")
df_disland["ID"] = df_disland["DispID"].map(str) + "." + df_disland["LandID"].map(str) + "." + df_disland["PhaseID"].map(str)
df_disland["PID"] = df_disland["DispID"]
col_disland = ["LandID","DispID","PhaseID","ID","PID","LandValue","Improvements","NegotiatedPrice","PresentYear","MVPresentYear","ValuationOption","ValuationType","CDate","MDate","CUser","MUser"]
df_disland = df_disland.reindex(columns=col_disland)
dfdis = pd.read_csv("{}".format(sd) + "csvDisList.csv", sep=";", dtype={'YearDispossession': str})
df_dis = dfdis.fillna("")
dfclmdis = pd.read_csv("{}".format(sd) + "csvClaimDisLink.csv", sep=";", dtype={'PresentYear': str})
df_clmdis = dfclmdis.fillna("")
df_clmdis["ID"] = df_clmdis["ClaimID"].map(str) + "." + df_clmdis["DispID"].map(str)
df_clmdis["PID"] = df_clmdis["ClaimID"]
col_clmdis = ["DispID","ClaimID","ID","PID","ValuationOption","ValuationType","PresentYear","CPIPresentYear","CPIDispossessedYear","MVDispossessedYear","MVPresentYear","SSO","SSOHousingQuantum","SSONoHH","CDate","MDate","Cuser","Muser"]
df_clmdis = df_clmdis.reindex(columns=col_clmdis)



df_land.to_sql('tblLandList', conn, if_exists='replace', index=False, chunksize=10000)
df_disland.to_sql('tblDisLandLink', conn, if_exists='replace', index=False, chunksize=10000)
df_dis.to_sql('tblDisList', conn, if_exists='replace', index=False, chunksize=10000)
df_clmdis.to_sql('tblClaimDisLink', conn, if_exists='replace', index=False, chunksize=10000)


'''
#delete unlinked record
df_newlist = pd.merge(df_land, df_disland, how="left", on=["LandID"], indicator=True)
df_newlist.sort_values(by=['LandID'], inplace=True, ascending=False)
newlistopt = df_newlist.values.tolist()

newrec = []
lastcol = len(df_newlist.columns)-1
for i in newlistopt:
        if i[lastcol] == "left_only":
            newrec.append(i[0])
            cur.execute("DELETE FROM tblLandList WHERE LandID=?", (i[0],))
conn.commit()


##UNIQUE ID DISLANDLINK



##UNIQUE ID CLAIMDISLINK

queryoutlist = "SELECT * FROM tblLandList"
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



cur.execute("SELECT * FROM tblLandList")
records1 = cur.fetchall()
print(records1)

'''
cur.execute("SELECT * FROM tblDisLandLink")
records2 = cur.fetchall()
print(records2)
'''

cur.execute("SELECT * FROM tblDisList")
records3 = cur.fetchall()
print(records3)


cur.execute("SELECT * FROM tblClaimDisLink")
records4 = cur.fetchall()
print(records4)


querylistlink = "SELECT tblClaimDisLink.ClaimID, tblClaimDisLink.DispID, tblLandList.LandID, tblLandList.LandType, tblLandList.FarmErfNumber, tblLandList.PortionNumber, \
        tblLandList.FarmTownshipName, tblLandList.Extent, tblLandList.LocalAuthority, tblLandList.RegDivision, tblLandList.Province, tblLandList.DistrictMunicipality, \
        tblLandList.PreviousDescription, tblLandList.LPICode, tblLandList.Extent_Measure, tblLandList.Hectares, tblLandList.SquareMeters, tblLandList.CurrentLandUse, \
        tblLandList.TitleDeedNumber, tblLandList.PropertyOwnerType, tblLandList.OwnerName, tblLandList.IdentityNo, tblLandList.TelNumber, tblLandList.CellNumber, \
        tblLandList.MultipleOwners, tblLandList.MultipleProperties, tblLandList.Comments, tblLandList.LotNumber, tblLandList.Unregistered, \
        tblLandList.ClaimLand_Status, tblLandList.Latitude, tblLandList.Longitude, \
        IIf(tblLandList.LotNumber Is Not Null, 'Lot ' & tblLandList.LotNumber & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True, ' (Unregistered piece of land)', ''), 'Portion ' & tblLandList.PortionNumber & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True, ' (Unregistered piece of land)', '')) AS LandName, \
        IIf(tblLandList.LotNumber Is Not Null, 'Lot ' & tblLandList.LotNumber & IIf(tblLandList.SubNumber Is Not Null,' (Sub ' & tblLandList.SubNumber & ')', '') & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True,' (Unregistered piece of land)', '') & IIf(tblLandList.ClaimLand_Status='Alternative Land',' (Alternative Land)', ''), 'Portion ' & tblLandList.PortionNumber & IIf(tblLandList.SubNumber Is Not Null,' (Sub ' & tblLandList.SubNumber & ')', '') & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True,' (Unregistered piece of land)', '') & IIf(tblLandList.ClaimLand_Status='Alternative Land',' (Alternative Land)', '')) AS LandName_Extended, \
        IIf(tblLandList.Extent_Measure='Hectares', Extent, Extent/10000) AS Extent_Ha \
        FROM (tblDisList LEFT JOIN (tblDisLandLink LEFT JOIN tblLandList ON tblDisLandLink.LandID = tblLandList.LandID) ON tblDisList.DispID = tblDisLandLink.DispID) \
        INNER JOIN (tblClaimList LEFT JOIN tblClaimDisLink ON tblClaimList.ClaimID = tblClaimDisLink.ClaimID) ON tblDisList.DispID = tblClaimDisLink.DispID \
        WHERE (tblLandList.LandID Is Not Null) \
        ORDER BY tblLandList.LandID DESC"
cur.execute(querylistlink)
linkchildrows = cur.fetchall()
print(linkchildrows)



IIf(tblLandList.LotNumber Is Not Null,'Lot' & ' ' & tblLandList.LotNumber & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True,' (Unregistered piece of land)',''),'Portion' & ' ' & tblLandList.PortionNumber & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True,' (Unregistered piece of land)','')) AS LandName, \
        IIf(tblDisLandLink.DispID Is Not Null,DCount('DispID','tblDisLandLink','DispID = ' & tblDisLandLink.DispID)- DCount('DispID','tblDisLandLink','DispID = ' & tblDisLandLink.DispID & ' AND  Land_ID > ' & tblDisLandLink.LandID),) AS ID_Sort, \
        IIf(tblLandList.LotNumber Is Not Null,'Lot' & ' ' & tblLandList.LotNumber & IIf(tblLandList.SubNumber Is Not Null,' (Sub ' & tblLandList.SubNumber & ')','') & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True,' (Unregistered piece of land)','') & IIf(tblLandList.ClaimLand_Status='Alternative Land',' (Alternative Land)',''),'Portion' & ' ' & tblLandList.PortionNumber & IIf(tblLandList.SubNumber Is Not Null,' (Sub ' & tblLandList.SubNumber & ')', '') & ' of ' & tblLandList.LandType & ' ' & tblLandList.FarmErfNumber & ' ' & tblLandList.FarmTownshipName & IIf(tblLandList.Unregistered=True,' (Unregistered piece of land)', '') & IIf(tblLandList.ClaimLand_Status='Alternative Land',' (Alternative Land)', '')) AS LandName_Extended, \
        FormatNumber(IIf(tblLandList.Extent_Measure='Hectares', Extent,Extent/10000),4) AS Extent_Ha, \
'''
conn.close()