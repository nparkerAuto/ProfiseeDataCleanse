import pandas as pd

df_profisee_char=pd.read_excel('C:\\Users\\NParker\\Documents\\Profisee_char_list.xlsx')
df_profisee_abbrev=pd.read_excel('C:\\Users\\NParker\\Documents\\Profisee_Abbrev_List.xlsx')
df_sap_abbrev=pd.read_excel("C:\\Users\\NParker\\Documents\\SAP_Abbrev_List.xlsx")
df_class_list=pd.read_excel("C:\\Users\\NParker\\Documents\\Seed_Class_List.xlsx")


def prof_char_dict_generator(char_df):
	char_dict={}
	for index, row in char_df.iterrows():
		char_dict[row["Abbreviation"]]=row["IngredientType"]
	return char_dict
prof_char_dict=prof_char_dict_generator(df_profisee_char)

def prof_ab_dict_generator(char_df):
	char_dict={} 
	for index, row in char_df.iterrows():
		char_dict[row["Abbreviation"]]=row["Abbreviated Word"]
	return char_dict
prof_abbrev_dict=prof_ab_dict_generator(df_profisee_abbrev)

def sap_ab_dict_generator(char_df):
	char_dict={}
	for index, row in char_df.iterrows():
		char_dict[row["Abbreviated Word"]]=row["Abbreviation"]
	return char_dict
sap_abbrev_dict=sap_ab_dict_generator(df_sap_abbrev)

def prof_class_list_generator(char_df):
    classList=[]
    for index,row in char_df.iterrows():
        classList.append({"ABBREVIATION":row["ABBREVIATION"], "NOUN":row["NOUN"], "NOUNMODIFIER":row["NOUNMODIFIER"], "CLASS":row["CLASS"]})
    return classList  
prof_class_list=prof_class_list_generator(df_class_list)    

def findItem(nounMod):
    for item in prof_class_list:
        if item["ABBREVIATION"]==nounMod:
            return item["NOUN"], item["NOUNMODIFIER"], item["CLASS"]
    return "notfound","notfound","notfound"
    
def abbrev_check(val, abbrev_dict):
    val_new=val
    if val in abbrev_dict:
        val_new=abbrev_dict[val]
    return val_new
