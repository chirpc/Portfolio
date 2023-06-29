
from ast import Is, IsNot, Str
from asyncio.windows_events import NULL
from cmath import isnan, nan
import os
from pickle import FALSE, NONE
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import csv
from datetime import datetime, date, time, timedelta
from scipy import stats
import igraph as ig
##########################################
from ast import Is, IsNot
from asyncio.windows_events import NULL
import os
from pickle import NONE
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from numpy import random as nprando
import csv
from datetime import datetime, date, time, timedelta
from scipy import stats
import igraph as ig
from sklearn.preprocessing import LabelEncoder



#######################################################################
##NETWORK TRAVERSAL##

#FUNCTIONS

def get_odi(G,o_lst):
    e_odi_dict={}
    for o in o_lst:
        e_odi_lst = list(nx.dfs_preorder_nodes(G, source=o))
        e_odi_dict[o] = e_odi_lst

    return e_odi_dict
get_odi(G_tree,['1187.14463.1','1187.14447.1'])

def get_descendants(G,s):
    """

    Using networkx to find direct descendents of parent nodes.
    Create dictionary of deceased parents with list of eligible descendents
    G = graph
    s = claim

    """
    e_ben_dict={}
    parent = list([str(s)])
    while(1):
        if len(parent) == 0:
            return e_ben_dict
        e_ben_lst = []
        tmp_d = []
        for each in parent:
            ben_lst = list(G.successors(str(each)))
            for ben in ben_lst:
                # if eligible -> create a list of children for deceased parent
                if ben_dict[ben]["Eligible"] == True :
                    e_ben = (each, ben)
                    e_ben_lst.append(e_ben)
                    # if deceased or odi spouse -> find children
                    if ben_dict[ben]["Deceased"] == True or ben_dict[ben]["RelationshipID"] == "2" :
                        tmp_d.append(ben)
        parent = list(tmp_d)
        for k,v in e_ben_lst:
            e_ben_dict.setdefault(k, []).append(v)
#descendants(G_tree, '1187')

#Calculate share of award for grand descendants
def share_ben(claim,ben,award,share=None):
    """
    Using dictionary of lists to calculate the share of award to eligible beneficiaries.
    Create list of tuples of award share and amount to eligible beneficiaries.

    """
    award_lst = []
    parent_lst = list([(ben,share,award)])
    e_tree = get_descendants(G_tree,str(claim))
    while(1):
        if len(parent_lst) == 0:
            return award_lst
        d_ben_lst =[]    
        for parent,share,award in parent_lst:
            e_ben_lst = e_tree.get(str(parent),None)
            #print(e_ben_lst)
            # if deceased parent has no eligible descendents -> mark as not eligible
            if e_ben_lst is None:
                #print("Warning: " + parent + " is eligible and deceased with no eligible descendants!")
                note = "Not Eligible"
                comment = "Warning: ben is eligible and deceased with no eligible descendants!"
                tot_e_ben = (parent,share,award,note,comment)
                award_lst.append(tot_e_ben)
            else:
                tot_e_award = 0
                tot_e_award_lst = []
                tmp=[]
                for e_ben in e_ben_lst:
                    # if eligible -> calculate share
                    if ben_dict[e_ben]['Eligible'] == True:
                        rid = ben_dict[e_ben]['RelationshipID']
                        #print(rid)
                        no_e_ben = len(e_ben_lst)
                        share_e_ben = 1/no_e_ben
                        award_e_ben = award*(1/no_e_ben)
                        comment_e_ben = ""

                        # special case: if odi spouse alive and has child -> calculate share 
                        if rid == "2":
                            if ben_dict[e_ben]['Deceased'] == False:
                                child_lst = e_tree.get(str(e_ben),None)
                                if child_lst is not None:
                                    no_child = len(child_lst)
                                    award_spouse = calc_share(claim,e_ben,no_e_ben,award,parent,rid,no_child)
                                    if award_spouse is not None:
                                        for s_s,a_s,c_s in award_spouse:
                                            share_e_ben = s_s
                                            award_e_ben = a_s
                                            comment_e_ben = c_s
                                    d_ben = (e_ben,share_e_ben,award_e_ben)
                                    d_ben_lst.append(d_ben)

                        # special case: if child has parent alive -> calculate share 
                        elif rid == "3":
                            if ben_dict[parent]['Deceased'] == False:
                                award_child = calc_share(claim,e_ben,no_e_ben,award,parent,rid)
                                if award_child is not None:
                                    for s_c,a_c,c_c in award_child:
                                        share_e_ben = s_c
                                        award_e_ben = a_c
                                        comment_e_ben = c_c
                        # no special case
                        else:
                            pass

                        # if alive -> assign share
                        if ben_dict[e_ben]['Deceased'] == False: 
                            #print("ben alive", e_ben)
                            award_e_note = "Eligible"  
                            tot_e_ben = (e_ben,share_e_ben,award_e_ben,award_e_note,comment_e_ben)
                            tmp.append(tot_e_ben)
                            award_lst.append(tot_e_ben)
                        # if deceased -> find descendents
                        elif ben_dict[e_ben]['Deceased'] == True: 
                            #print("ben deceased", e_ben)
                            d_ben = (e_ben,share_e_ben,award_e_ben)
                            d_ben_lst.append(d_ben)

        parent_lst  = list(d_ben_lst)
#share_ben('235','235',100000.00)

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

    if rid == "2":
        #print("alive spouse has child")
        # if odi spouse was not present at dispossession -> assign odi spouse 50%
        if ben_dict[ben]['Dispossessed'] == False:
            #print("alive spouse not dispossessed")  
            comment_spouse = "Spouse + child alive with but spouse is not ODI"
            share_spouse = (1/no_ben)*0.5
            award_spouse = award*(1/no_ben)*0.5
            tot_spouse = (share_spouse,award_spouse,comment_spouse)

        # if odi spouse was present at dispossession -> assign odi spouse 50% + child share
        elif ben_dict[ben]['Dispossessed'] == True:
            #print("alive spouse dispossessed")  
            comment_spouse = "Spouse + child alive and spouse is ODI"
            share_spouse = (1/no_ben)*0.5*(1+(1/(no_child + 1)))
            award_spouse = award*(1/no_ben)*0.5*(1+(1/(no_child + 1)))
            tot_spouse = (share_spouse,award_spouse,comment_spouse)
        tmp.append(tot_spouse)

    elif rid == "3":
        # if odi spouse was not present at dispossession -> assign child 50%
        if ben_dict[parent]['Dispossessed'] == False:
            #print("alive spouse not dispossessed + child")  
            comment_child = "Child + spouse alive but spouse is not ODI"
            share_child = (1/no_ben)
            award_child = award*(1/no_ben)
            tot_child = (share_child,award_child,comment_child)

        # if odi spouse was present at dispossession -> assign child 50% minus odi spouse share
        elif ben_dict[parent]['Dispossessed'] == True:
            #print("alive spouse dispossessed + child") 
            comment_child = "Child + spouse alive and is ODI"
            share_child = (1/(no_ben + 1))
            award_child = award*(1/(1+(1/(no_ben + 1))))*(1/(no_ben + 1))
            tot_child = (share_child,award_child,comment_child)
        tmp.append(tot_child)
                
    return tmp


#############################################################################
##EXECUTE TRAVERSAL

#FIN COMP
#print(e_tree['235'])
#print(share_ben('235','235',100000.00))

#o_tree = {} 
for claim,award in fin_lst:
    if G_tree.has_node(str(claim)): 
        #find odi
        #for odi in list(G_tree.successors(str(claim))):
        o_tree = get_odi(G_tree, list(G_tree.successors(str(claim))))
        #print(o_tree)
        df_odi_fin = pd.DataFrame.from_dict(o_tree, orient='index').reset_index()
        #print(df_odi_fin)
        df_odi_fin =pd.melt(df_odi_fin, id_vars='index').sort_values(by=['index','value'], ascending=True)
        #print(df_odi_fin)
        df_odi_fin = df_odi_fin.dropna(subset=['value'])
        #print(df_odi_fin)
        df_odi_fin = df_odi_fin[['index','value']].rename(columns={'index':'odi_id','value':'id'})
        df_odi_fin = pd.merge(df_odi_fin, df_linklist[['ClaimID','ID','LastName','FirstName']], how='left', left_on='odi_id', right_on='ID')
        #print(df_odi_fin)
        df_odi_fin = df_odi_fin[['ClaimID','id','odi_id','LastName','FirstName']].rename(columns={'LastName':'odi_lastname','FirstName':'odi_firstname'})
        #print(df_odi_fin.info())

        #find descendants
        e_tree = get_descendants(G_tree,str(claim))
        #print(e_tree)
        df_desc_fin = pd.DataFrame.from_dict(e_tree, orient='index').reset_index()
        #print(df_desc_fin)
        df_desc_fin =pd.melt(df_desc_fin, id_vars='index').sort_values(by=['index','value'], ascending=True)
        #print(df_desc_fin)
        df_desc_fin = df_desc_fin.dropna(subset=['value'])
        #print(df_desc_fin)
        
        #find award
        s_tree = share_ben(str(claim),str(claim),float(award))
        #c_tree[str(claim)] = s
        #print(c_tree)
        df_share= pd.DataFrame(s_tree, columns=['id','share','award','status','comment'])
        
        #export odi 
        df_edge_odi2 = df_edge_odi[['source', 'target','odi_lname','claim_source']].loc[(df_edge_odi['claim_source']==str(claim)) & (df_edge_odi['claim_target']==str(claim)),:]
        df_edge_odi2 = df_edge_odi2.loc[df_edge_odi2['odi_lname']==1,:]
        df_edge_odi2.to_csv(opth + "sna_odi_"+str(claim)+".csv",sep=',',encoding='utf-8', index=False)

        #export edge
        #df_edge_fin = df_desc_fin[['index','value']].rename(columns={'index':'source','value':'target'})
        df_edge_fin = df_linklist[['ID','PID','ClaimID']].loc[df_linklist['ClaimID']==str(claim),:]
        df_edge_fin = df_edge_fin.rename(columns={'PID':'source','ID':'target'})
        df_edge_fin = df_edge_fin.dropna(subset=["target"])
        df_edge_fin.to_csv(opth + "sna_edge_fin_"+str(claim)+".csv",sep=',',encoding='utf-8', index=False)

        #export attr
        #df_attr_fin= df_linklist.loc[df_linklist['ClaimID']==str(claim),:]
        df_attr_fin = pd.merge(df_odi_fin, df_linklist, how='left', left_on=['ClaimID','id'], right_on=['ClaimID','ID'])
        df_attr_fin = pd.merge(df_attr_fin, df_share, how='left', left_on='id', right_on='id')
        #print(df_attr_fin.info())
        df_attr_fin['award'] = df_attr_fin['award'].round(2)
        df_attr_fin['l_award'] = np.log2(df_attr_fin['award'])
        df_attr_fin['l_award'] = np.where(df_attr_fin['l_award'].isnull(),0,df_attr_fin['l_award'])
        df_attr_fin = df_attr_fin.drop(columns='ID')
        print(df_attr_fin.info())
        df_attr_fin.to_csv(opth + "sna_attr_fin_"+str(claim)+".csv",sep=',',encoding='utf-8', index=False)


#LAND RESTORE
l_tree ={}
for claim,hectare in land_lst:
    if G_tree.has_node(str(claim)): 
        #find odi
        #for odi in list(G_tree.successors(str(claim))):
        o_tree = get_odi(G_tree, list(G_tree.successors(str(claim))))
        #print(o_tree)
        df_odi_land = pd.DataFrame.from_dict(o_tree, orient='index').reset_index()
        #print(df_odi_fin)
        df_odi_land =pd.melt(df_odi_land, id_vars='index').sort_values(by=['index','value'], ascending=True)
        #print(df_odi_fin)
        df_odi_land = df_odi_land.dropna(subset=['value'])
        #print(df_odi_fin)
        df_odi_land = df_odi_land[['index','value']].rename(columns={'index':'odi_id','value':'id'})
        df_odi_land = pd.merge(df_odi_land, df_linklist[['ClaimID','ID','LastName','FirstName']], how='left', left_on='odi_id', right_on='ID')
        #print(df_odi_fin)
        df_odi_land = df_odi_land[['ClaimID','id','odi_id','LastName','FirstName']].rename(columns={'LastName':'odi_lastname','FirstName':'odi_firstname'})
        #print(df_odi_fin.info())
        #find descendents 
        e_tree = get_descendants(G_tree,str(claim))
        #print(e_tree)
        df_edge_land = pd.DataFrame.from_dict(e_tree, orient='index').reset_index()
        #print(df_edge_land)
        df_edge_land =pd.melt(df_edge_land, id_vars='index').sort_values(by=['index','value'], ascending=True)
        #print(df_edge_land)

        #export odi 
        df_edge_odi2 = df_edge_odi[['source', 'target','odi_lname','claim_source']].loc[(df_edge_odi['claim_source']==str(claim)) & (df_edge_odi['claim_target']==str(claim)),:]
        df_edge_odi2 = df_edge_odi2.loc[df_edge_odi2['odi_lname']==1,:]
        df_edge_odi2.to_csv(opth + "sna_odi_"+str(claim)+".csv",sep=',',encoding='utf-8', index=False)


        #export edge
        #df_edge_land = df_linklist1[['index','value']].rename(columns={'index':'source','value':'target'})
        df_edge_land = df_linklist[['ID','PID','ClaimID']].loc[df_linklist['ClaimID']==str(claim),:]
        df_edge_land = df_edge_land.rename(columns={'PID':'source','ID':'target'})
        df_edge_land = df_edge_land.dropna(subset=["target"])
        df_edge_land.to_csv(opth + "sna_edge_land_"+str(claim)+".csv",sep=',',encoding='utf-8', index=False)

        #export attr
        df_attr_land = pd.merge(df_odi_land, df_linklist, how='left', left_on=['ClaimID','id'], right_on=['ClaimID','ID'])
        df_attr_land = df_attr_land.loc[df_attr_land['ClaimID']==str(claim),:]
        df_attr_land.rename(columns={'ID':'id'}).to_csv(opth + "sna_attr_land_"+str(claim)+".csv",sep=',',encoding='utf-8', index=False)


df_list.to_csv(opth + "sna_attr.csv",sep=',',encoding='utf-8', index=False)
df_link.rename(columns={'PID':'source','ID':'target'}).to_csv(opth + "sna_edge.csv",sep=',',encoding='utf-8', index=False)
