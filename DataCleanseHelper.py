#This script takes in excel documents and converts them to a dictionary
import pandas as pd

df_profisee_char=pd.read_excel('C:\\Users\\Nora.Parker\\Documents\\Profisee_char_list.xlsx')
df_profisee_abbrev=pd.read_excel('C:\\Users\\Nora.Parker\\Documents\\Profisee_Abbrev_List.xlsx')
df_sap_abbrev=pd.read_excel("C:\\Users\\Nora.Parker\\Documents\\SAP_Abbrev_List.xlsx")

def prof_char_dict_generator(char_df):
	char_dict={}
	for index, row in char_df.iterrows():
		char_dict[row["Abbreviation"]]=row["IngredientType"]
		char_dict[row["Abbreviated Word"]]=row["IngredientType"]
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

#Abbreviation --> Abbreviated Word	
def abbrev_check(val, abbrev_dict):
	if val in abbrev_dict:
		val=abbrev_dict[val]
	return val
	
	
def create_descriptions(char_dict):
	PO_Desc=""
	Long_Desc=""
	for key in char_dict:
		val=char_dict[key]
		char_dict[key]=abbrev_check(val, prof_abbrev_dict)
		if key=="NOUN":
			PO_Desc=char_dict[key]+":"
			Long_Desc=char_dict[key]+":"
		elif key=="NOUN MODIFIER":
			PO_Desc+=char_dict[key]+";"
			Long_Desc+=char_dict[key]+";"
		else:
			PO_Desc+=key+":"+char_dict[key]+", "
			Long_Desc+=char_dict[key]+", "
	short_desc=create_short_desc(char_dict)	
	return short_desc, Long_Desc[:len(Long_Desc)-2], PO_Desc[:len(PO_Desc)-2]
	
def consolidate_Desc(attribute_Dict):
	attribute_dict_short={}
	
	for key in attribute_Dict:
		key_abvr=sap_abbrev_dict[key]
		if attribute_Dict[key] in sap_abbrev_dict:
			value_abvr=sap_abbrev_dict[attribute_Dict[key]]
			attribute_dict_short[key_abvr]=value_abvr
		else:
			attribute_dict_short[key_abvr]=attribute_Dict[key]
	return attribute_dict_short
	
def short_desc_helper(desc_dict):
	short_desc=""
	for key in desc_dict:
		if key=="NOUN":
			short_desc=desc_dict[key]+":"
		elif key=="NOUN MODIFIER":
			short_desc+=desc_dict[key]+";"
		else:
			short_desc+=key+":"+desc_dict[key]+", "
			
	return short_desc[:len(short_desc)-2]
	
def create_short_desc(attribute_Dict):
	short_desc_dict=consolidate_Desc(attribute_Dict)
	
	short_desc=short_desc_helper(short_desc_dict)
	
	while len(short_desc)>39:
		short_desc_dict.popitem()
		short_desc=short_desc_helper(short_desc_dict)
	
	return short_desc
	
def format1_cleanse(row, noun, nounMod,legacy_num, sap_class):

	attribute_Dict={}
	attribute_List=[]

	attribute_Dict["NOUN"]=noun
	attribute_Dict["NOUN MODIFIER"]=abbrev_check(nounMod,prof_abbrev_dict)
	
	attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"NOUN", "Characteristic Description":attribute_Dict["NOUN"]})
	attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"NOUN_MODIFIER", "Characteristic Description":attribute_Dict["NOUN MODIFIER"]})
		
	try:
		char_group=str(row["Name"][5:31])
		group_list=char_group.split()
		
		for i in range(0,len(group_list)):
			if group_list[i] in prof_char_dict:
				if prof_char_dict[group_list[i]]=="6":
					attribute_Dict["SEED TRAIT"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_TRAIT", "Characteristic Description":attribute_Dict["SEED TRAIT"]}) 
				if prof_char_dict[group_list[i]]=="7":
					attribute_Dict["SEED SIZE"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_SIZE", "Characteristic Description":attribute_Dict["SEED SIZE"]})
				if prof_char_dict[group_list[i]]=="8" or prof_char_dict[group_list[i]]=="11":
					attribute_Dict["SEED TREATMENT"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_TREATMENT", "Characteristic Description":attribute_Dict["SEED TREATMENT"],"Short Description (SAP)": Short_Desc, "Long Description (SAP)":Long_Desc, "PO Description (SAP)":PO_Desc})
			elif i==0:
				attribute_Dict["SEED VARIETY"]=abbrev_check(group_list[i], prof_abbrev_dict)
				attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_VARIETY", "Characteristic Description":attribute_Dict["SEED VARIETY"]})
			else:
				attribute_List_eject=[{"Legacy Number":legacy_num, "Characteristic":group_list[i], "Characteristic Description":"DOES NOT FOLLOW FORMAT: CHAR COULD NOT BE IDENTIFIED", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
				return attribute_List_eject
				
		
		seed_package_configuration=row["Name"][33:41].strip()
		if seed_package_configuration!="":
			attribute_Dict["SEED PACKAGE CONFIGURATION"]=abbrev_check(seed_package_configuration, prof_abbrev_dict)
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_PACKAGE_CONFIGURATION", "Characteristic Description":attribute_Dict["SEED PACKAGE CONFIGURATION"]}) 
		brand=row["Name"][42:50].strip()
		if brand!="":
			attribute_Dict["BRAND"]=abbrev_check(brand, prof_abbrev_dict)
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"BRAND", "Characteristic Description":attribute_Dict["BRAND"]})
		#Getting Descriptions		
		short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
		
		for row in attribute_List:
			row["Short Description (SAP)"]=short_desc
			row["Long Description (SAP)"]=Long_Desc
			row["PO Description (SAP)"]=PO_Desc
			row["SAP Class"]=sap_class
			 
		return attribute_List
		
	except IndexError:
		attribute_List_eject=[{"Legacy Number":legacy_num, "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
		return attribute_List_eject

def format2_cleanse(row, noun, nounMod,legacy_num, sap_class):
	attribute_Dict={}
	attribute_List=[]

	attribute_Dict["NOUN"]=noun
	attribute_Dict["NOUN MODIFIER"]=nounMod
	
	attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"NOUN", "Characteristic Description":attribute_Dict["NOUN"]})
	attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"NOUN_MODIFIER", "Characteristic Description":attribute_Dict["NOUN MODIFIER"]})
		
	seed_variety=""
	try:
		char_group=str(row["Name"][5:31])
		group_list=char_group.split()
		
		for i in range(0,len(group_list)):
			if group_list[i] in prof_char_dict:
				if prof_char_dict[group_list[i]]=="6":
					attribute_Dict["SEED TRAIT"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_TRAIT", "Characteristic Description":attribute_Dict["SEED TRAIT"]}) 
				if prof_char_dict[group_list[i]]=="7":
					attribute_Dict["SEED SIZE"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_SIZE", "Characteristic Description":attribute_Dict["SEED SIZE"]})
				if prof_char_dict[group_list[i]]=="8":
					attribute_Dict["SEED TREATMENT"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_TREATMENT", "Characteristic Description":attribute_Dict["SEED TREATMENT"],"Short Description (SAP)": Short_Desc, "Long Description (SAP)":Long_Desc, "PO Description (SAP)":PO_Desc})
			elif i==0:
				seed_variety=str(group_list[i])
			else:
				seed_variety+=" "+str(group_list[i])
		if seed_variety!="":		
			attribute_Dict["SEED VARIETY"]=abbrev_check(seed_variety, prof_abbrev_dict)	
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_VARIETY", "Characteristic Description":attribute_Dict["SEED VARIETY"]})		
		
		seed_package_configuration=row["Name"][33:41].strip()
		if seed_package_configuration!="":
			attribute_Dict["SEED PACKAGE CONFIGURATION"]=abbrev_check(seed_package_configuration, prof_abbrev_dict)
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_PACKAGE_CONFIGURATION", "Characteristic Description":attribute_Dict["SEED PACKAGE CONFIGURATION"]}) 
		brand=row["Name"][42:50].strip()
		if brand!="":
			attribute_Dict["BRAND"]=abbrev_check(brand, prof_abbrev_dict)
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"BRAND", "Characteristic Description":attribute_Dict["BRAND"]})
		#Getting Descriptions		
		short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
		
		for row in attribute_List:
			row["Short Description (SAP)"]=short_desc
			row["Long Description (SAP)"]=Long_Desc
			row["PO Description (SAP)"]=PO_Desc
			row["SAP Class"]=sap_class
			 
		return attribute_List
		
	except IndexError:
		attribute_List_eject=[{"Legacy Number":legacy_num, "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
		return attribute_List_eject
		
def format3_cleanse(row, noun, nounMod,legacy_num,sap_class):
	attribute_Dict={}
	attribute_List=[]

	attribute_Dict["NOUN"]=noun
	attribute_Dict["NOUN MODIFIER"]=nounMod
	
	attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"NOUN", "Characteristic Description":attribute_Dict["NOUN"]})
	attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"NOUN_MODIFIER", "Characteristic Description":attribute_Dict["NOUN MODIFIER"]})
		
	seed_variety=""
	try:
		char_group=str(row["Name"][5:31])
		group_list=char_group.split()
		
		for i in range(0,len(group_list)):
			if group_list[i] in prof_char_dict:
				if prof_char_dict[group_list[i]]=="6":
					attribute_Dict["SEED CLASS"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_CLASS", "Characteristic Description":attribute_Dict["SEED CLASS"]}) 
				if prof_char_dict[group_list[i]]=="7":
					attribute_Dict["SEED SIZE"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_SIZE", "Characteristic Description":attribute_Dict["SEED SIZE"]})
				if prof_char_dict[group_list[i]]=="8":
					attribute_Dict["SEED TREATMENT"]=abbrev_check(group_list[i], prof_abbrev_dict)
					attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_TREATMENT", "Characteristic Description":attribute_Dict["SEED TREATMENT"]})
			elif i==0:
				seed_variety=str(group_list[i])
			else:
				seed_variety+=" "+str(group_list[i])
		if seed_variety!="":		
			attribute_Dict["SEED VARIETY"]=abbrev_check(seed_variety, prof_abbrev_dict)	
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_VARIETY", "Characteristic Description":attribute_Dict["SEED VARIETY"]})		
		
		seed_package_configuration=row["Name"][33:41].strip()
		if seed_package_configuration!="":
			attribute_Dict["SEED PACKAGE CONFIGURATION"]=abbrev_check(seed_package_configuration, prof_abbrev_dict)
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"SEED_PACKAGE_CONFIGURATION", "Characteristic Description":attribute_Dict["SEED PACKAGE CONFIGURATION"]}) 
		brand=row["Name"][42:50].strip()
		if brand!="":
			attribute_Dict["BRAND"]=abbrev_check(brand, prof_abbrev_dict)
			attribute_List.append({"Legacy Number":legacy_num, "Characteristic":"BRAND", "Characteristic Description":attribute_Dict["BRAND"]})
		#Getting Descriptions		
		short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
		
		for row in attribute_List:
			row["Short Description (SAP)"]=short_desc
			row["Long Description (SAP)"]=Long_Desc
			row["PO Description (SAP)"]=PO_Desc
			row["SAP Class"]=sap_class
			 
		return attribute_List
		
	except IndexError:
		attribute_List_eject=[{"Legacy Number":legacy_num, "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
		return attribute_List_eject	
