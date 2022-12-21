import pandas as pd

from SAPCharacteristics import seedVariety_1,seedTrait,seedClass,seedSize,seedTrait,seedTreatment,additionalFeat,seedBrand,seedPackageSize
from SAPCharacteristics import fertAddFact, fertBrand, fertForm, fertPackageConfig, fertPercent, fertProduct
from AbbrevAndChar import abbrev_check, prof_char_dict, prof_abbrev_dict
from Descriptions import create_descriptions

notValidList=["&", "/", ".", ",","#"]

def format1_cleanse(row, noun, nounMod,legacy_num, sap_class):

    attribute_Dict={}
    attribute_List=[]

    attribute_Dict["NOUN"]=noun
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":attribute_Dict["NOUN"]})
    
    if nounMod!="nomod":
        attribute_Dict["NOUN MODIFIER"]=nounMod
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN_MODIFIER", "Characteristic Description":attribute_Dict["NOUN MODIFIER"]})
    
   
    trait_count=1
    size_count=1
    treat_count=1
    
    try:
        char_group=str(row["Name"][5:31])
        group_list=char_group.split()
        marker=len(group_list)
        
        for i in range(0,len(group_list)):
            if group_list[i] in prof_char_dict:
                if prof_char_dict[group_list[i]]==6:
                    attribute_Dict,attribute_List,trait_count, marker=seedTrait(attribute_Dict, attribute_List, group_list[i], marker, trait_count,row,legacy_num,i)
                   
                if prof_char_dict[group_list[i]]==7:
                    attribute_Dict,attribute_List,size_count, marker=seedSize(attribute_Dict, attribute_List, group_list[i], marker, size_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==8:
                    attribute_Dict,attribute_List,treat_count, marker=seedTreatment(attribute_Dict, attribute_List, group_list[i], marker, treat_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==12:
                    attribute_Dict, attribute_List, marker=additionalFeat(attribute_Dict, attribute_List, group_list[i], marker,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==16:
                    attribute_Dict,attribute_List=seedVariety_1(attribute_Dict,attribute_List, group_list[i],row,legacy_num)
                    
            elif i==0:
                attribute_Dict,attribute_List=seedVariety_1(attribute_Dict,attribute_List, group_list[i],row,legacy_num)
               
            else:
                attribute_List_eject=[{"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":group_list[i], "Characteristic Description":"DOES NOT FOLLOW FORMAT: CHAR COULD NOT BE IDENTIFIED", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
                return attribute_List_eject
				
		
        attribute_Dict, attribute_List=seedPackageSize(attribute_Dict,attribute_List,row,legacy_num) 
        attribute_Dict,attribute_List=seedBrand(attribute_Dict, attribute_List,row,legacy_num)
            
		#Getting Descriptions		
        short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
		
        for r in attribute_List:
            r["Short Description (SAP)"]=short_desc
            r["Long Description (SAP)"]=Long_Desc
            r["PO Description (SAP)"]=PO_Desc
            r["SAP Class"]=sap_class
			 
        return attribute_List
		
    except IndexError:
    	attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
    	return attribute_List_eject

def format2_cleanse(row, noun, nounMod,legacy_num, sap_class):
    attribute_Dict={}
    attribute_List=[]
    
    attribute_Dict["NOUN"]=noun
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":attribute_Dict["NOUN"]})
    
    if nounMod!="nomod":
        attribute_Dict["NOUN MODIFIER"]=nounMod
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN_MODIFIER", "Characteristic Description":attribute_Dict["NOUN MODIFIER"]})
		
    trait_count=1
    size_count=1
    treat_count=1
    
    seed_variety=""
    try:
        char_group=str(row["Name"][5:31])
        group_list=char_group.split()
        marker=len(group_list)
        for i in range(0,len(group_list)):
            
            if group_list[i] in prof_char_dict:
                
                if prof_char_dict[group_list[i]]==6:
                    attribute_Dict,attribute_List,trait_count, marker=seedTrait(attribute_Dict, attribute_List, group_list[i], marker, trait_count,row,legacy_num,i)
                   
                if prof_char_dict[group_list[i]]==7:
                    attribute_Dict,attribute_List,size_count, marker=seedSize(attribute_Dict, attribute_List, group_list[i], marker, size_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==8:
                    attribute_Dict,attribute_List,treat_count, marker=seedTreatment(attribute_Dict, attribute_List, group_list[i], marker, treat_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==16:
                    attribute_Dict["SEED VARIETY"]=str(abbrev_check(group_list[i], prof_abbrev_dict))
                    seed_variety+=" "+attribute_Dict["SEED VARIETY"]
                    
            elif group_list[i] in notValidList:
                attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":group_list[i], "Characteristic Description":"DOES NOT FOLLOW FORMAT: CHAR COULD NOT BE IDENTIFIED", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
                return attribute_List_eject
                
            elif i==0:
                seed_variety+=str(group_list[i])
                
            elif i < marker:
                add=" "+str(group_list[i])
                seed_variety+=add
                
            else:
                attribute_List_eject=[{"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":group_list[i], "Characteristic Description":"DOES NOT FOLLOW FORMAT: CHAR COULD NOT BE IDENTIFIED", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
                return attribute_List_eject
        
        if seed_variety!="":		
            attribute_Dict["SEED VARIETY"]=str(abbrev_check(seed_variety, prof_abbrev_dict))
            seed_variety=attribute_Dict["SEED VARIETY"]
            if len(seed_variety)>30:
                seed_variety=seed_variety[:30]
            attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"SEED_VARIETY", "Characteristic Description":attribute_Dict["SEED VARIETY"]})		
		
        attribute_Dict, attribute_List=seedPackageSize(attribute_Dict,attribute_List,row,legacy_num) 
        attribute_Dict,attribute_List=seedBrand(attribute_Dict, attribute_List,row,legacy_num)
            
		#Getting Descriptions		
        short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
		
        for r in attribute_List:
            r["Short Description (SAP)"]=short_desc
            r["Long Description (SAP)"]=Long_Desc
            r["PO Description (SAP)"]=PO_Desc
            r["SAP Class"]=sap_class
			 
        return attribute_List
		
    except IndexError:
        attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
        return attribute_List_eject
		
def format3_cleanse(row, noun, nounMod,legacy_num,sap_class):
    attribute_Dict={}
    attribute_List=[]

    attribute_Dict["NOUN"]=noun
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":attribute_Dict["NOUN"]})
    
    if nounMod!="nomod":
        attribute_Dict["NOUN MODIFIER"]=nounMod
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN_MODIFIER", "Characteristic Description":attribute_Dict["NOUN MODIFIER"]})
		
    trait_count=1
    size_count=1
    treat_count=1
    class_count=1
    
    try:
        char_group=str(row["Name"][5:31])
        group_list=char_group.split()
        marker=len(group_list)
        
        for i in range(0,len(group_list)):
            if group_list[i] in prof_char_dict:
                if prof_char_dict[group_list[i]]==6:
                    attribute_Dict, attribute_List, class_count, marker=seedClass(attribute_Dict, attribute_List, group_list[i], marker, class_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==7:
                    attribute_Dict,attribute_List,size_count, marker=seedSize(attribute_Dict, attribute_List, group_list[i], marker, size_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==8:
                    attribute_Dict,attribute_List,treat_count, marker=seedTreatment(attribute_Dict, attribute_List, group_list[i], marker, treat_count,row,legacy_num,i)
                    
                if prof_char_dict[group_list[i]]==16:
                    attribute_Dict,attribute_List=seedVariety_1(attribute_Dict,attribute_List, group_list[i],row,legacy_num)
                    
            elif i==0:
                attribute_Dict,attribute_List=seedVariety_1(attribute_Dict,attribute_List, group_list[i],row,legacy_num)
            else:
                attribute_List_eject=[{"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":group_list[i], "Characteristic Description":"DOES NOT FOLLOW FORMAT: CHAR COULD NOT BE IDENTIFIED", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
                return attribute_List_eject
                
        attribute_Dict, attribute_List=seedPackageSize(attribute_Dict,attribute_List,row,legacy_num) 
        attribute_Dict,attribute_List=seedBrand(attribute_Dict, attribute_List,row,legacy_num)
            
		#Getting Descriptions		
        short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
		
        for r in attribute_List:
            r["Short Description (SAP)"]=short_desc
            r["Long Description (SAP)"]=Long_Desc
            r["PO Description (SAP)"]=PO_Desc
            r["SAP Class"]=sap_class
			 
        return attribute_List
		
    except IndexError:
        attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
        return attribute_List_eject	

def format_chem(row,legacy_num):
    attribute_Dict={}
    attribute_List=[]
    LiqList=["4H", "4I", "5K", "5R"]
    DryList=["4E","4J", "4K", "4L", "5I", "5S"]
    try:
        sap_class=""
        if row["ProductCategory"] in LiqList:
            sap_class="M_AG_CHEMICAL_LIQ"
        elif row["ProductCategory"] in DryList:
            sap_class="M_AG_CHEMICAL_DRY"
        else:
            attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Product Category NA", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Product Category", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
            return attribute_List_eject
           
        label_name=row["Name"][0:31].strip()
        package_size=row["Name"][33:40].strip()
        mfg=row["Name"][42:].strip()
        if row["Name"][32]==" " and row["Name"][41]==" ":
            if label_name!="":
                attribute_Dict["LABELED NAME"]=str(abbrev_check(label_name, prof_abbrev_dict))
                attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"LABELED_NAME", "Characteristic Description":attribute_Dict["LABELED NAME"]})
            if package_size!="":
                attribute_Dict["CHEM PACKAGE CONFIGURATION"]=str(abbrev_check(package_size, prof_abbrev_dict))
                attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"CHEM_PACKAGE_CONFIGURATION", "Characteristic Description":attribute_Dict["CHEM PACKAGE CONFIGURATION"]})
            if mfg!="":
                attribute_Dict["MANUFACTURER"]=str(abbrev_check(mfg, prof_abbrev_dict))
                attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"MANUFACTURER", "Characteristic Description":attribute_Dict["MANUFACTURER"]})
        else:
            attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Format Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Format Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
            return attribute_List_eject
        short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
        
        for r in attribute_List:
            r["Short Description (SAP)"]=short_desc
            r["Long Description (SAP)"]=Long_Desc
            r["PO Description (SAP)"]=PO_Desc
            r["SAP Class"]=sap_class
			 
        return attribute_List
        
    except IndexError:
        attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
        return attribute_List_eject	  

def format_Fert_Micro(row, legacy_num, sap_class):
    attribute_Dict={}
    attribute_List=[]
    charg_group=row["Name"][0:31]
    
    g_analysis=""
    form=""                
    
    try:
        if '%' in row["ItemDescriptionPart1"]:
            percent, product, add_fact= fert_perc_helper(row)
            
            attribute_Dict, attribute_List=fertProduct(attribute_Dict, attribute_List, row, legacy_num, product, sap_class)
            attribute_Dict, attribute_List=fertPercent(attribute_Dict, attribute_List, row, legacy_num, percent, sap_class)
            attribute_Dict, attribute_List=fertForm(attribute_Dict, attribute_List, row, legacy_num, sap_class)
            attribute_Dict, attribute_List=fertAddFact(attribute_Dict, attribute_List, row, legacy_num, sap_class, add_fact)
            attribute_Dict, attribute_List=fertPackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
            attribute_Dict, attribute_List=fertBrand(attribute_Dict, attribute_List, row, legacy_num, sap_class)   
            
        elif row["ItemDescriptionPart1"].count('-')<2:
            product=str(row["ItemDescriptionPart1"]).strip()
            attribute_Dict, attribute_List=fertProduct(attribute_Dict, attribute_List, row, legacy_num, product, sap_class)
            attribute_Dict, attribute_List=fertPackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
            attribute_Dict, attribute_List=fertBrand(attribute_Dict, attribute_List, row, legacy_num, sap_class)   
            
        else:
            attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Format Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Format Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
            return attribute_List_eject
        
        short_desc, Long_Desc, PO_Desc=create_descriptions(attribute_Dict)
        
        for r in attribute_List:
            r["Short Description (SAP)"]=short_desc
            r["Long Description (SAP)"]=Long_Desc
            r["PO Description (SAP)"]=PO_Desc
            r["SAP Class"]=sap_class
            
        return attribute_List
    except IndexError:
        attribute_List_eject=[{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"Index Error", "Characteristic Description":"DOES NOT FOLLOW FORMAT: Index Error", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
        return attribute_List_eject
        
def fert_perc_helper(row):
    
    pointer=row["Name"].rfind('%')
    temp_point=pointer
    percentList=[]    
    while row["Name"][pointer]!=" " and row["Name"][pointer]!="-" and pointer>-1:
        percentList.append(row["Name"][pointer])
        pointer-=1
    percent="".join(percentList[::-1])
    product=row["Name"][0:pointer].strip()
    add_fact=row["Name"][temp_point+1:31].strip()
    return percent,product,add_fact
    
