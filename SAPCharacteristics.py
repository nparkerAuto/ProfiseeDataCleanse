from AbbrevAndChar import abbrev_check, prof_abbrev_dict


def seedVariety_1(attribute_Dict,attribute_List, group_list_i,row,legacy_num):
    attribute_Dict["SEED VARIETY"]=str(abbrev_check(group_list_i, prof_abbrev_dict))
    seed_variety=attribute_Dict["SEED VARIETY"]
    if len(seed_variety)>30:
        seed_variety=seed_variety[:30]  
    attribute_List.append({"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":"SEED VARIETY", "Characteristic Description":seed_variety})
    return attribute_Dict, attribute_List
    
def seedSize(attribute_Dict, attribute_List, group_list_i, marker, size_count,row,legacy_num,i):
    attribute_Dict[f"SEED SIZE {size_count}"]=str(abbrev_check(group_list_i, prof_abbrev_dict))
    seed_size=attribute_Dict[f"SEED SIZE {size_count}"]
    if len(seed_size)>30:
        seed_size=seed_size[:30]
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"SEED_SIZE_{size_count}", "Characteristic Description":seed_size})
    marker=i
    size_count+=1
    return attribute_Dict, attribute_List, size_count, marker

def seedTrait(attribute_Dict, attribute_List, group_list_i, marker, trait_count,row,legacy_num,i):
    attribute_Dict[f"SEED TRAIT {trait_count}"]=str(abbrev_check(group_list_i, prof_abbrev_dict))
    seed_trait=attribute_Dict[f"SEED TRAIT {trait_count}"]
    if len(seed_trait)>30:
        seed_trait=seed_trait[:30]    
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"SEED_TRAIT_{trait_count}", "Characteristic Description":seed_trait}) 
    marker=i
    trait_count+=1
    return attribute_Dict, attribute_List, trait_count, marker

def seedTreatment(attribute_Dict, attribute_List, group_list_i, marker, treat_count,row,legacy_num,i):
    attribute_Dict[f"SEED TREATMENT {treat_count}"]=str(abbrev_check(group_list_i, prof_abbrev_dict))
    seed_treatment=attribute_Dict[f"SEED TREATMENT {treat_count}"]
    if len(seed_treatment)>30:
        seed_treatment=seed_treatment[:30] 
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"SEED_TREATMENT_{treat_count}", "Characteristic Description":seed_treatment})
    marker=i
    treat_count+=1
    return attribute_Dict, attribute_List,treat_count, marker
    
def seedClass(attribute_Dict, attribute_List, group_list_i, marker, class_count,row,legacy_num,i):
    attribute_Dict[f"SEED CLASS {class_count}"]=str(abbrev_check(group_list_i, prof_abbrev_dict))
    seed_class=attribute_Dict[f"SEED CLASS {class_count}"]
    if len(seed_class)>30:
        seed_class=seed_class[:30]
    attribute_List.append({"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":f"SEED_CLASS_{class_count}", "Characteristic Description":seed_class})
    class_count+=1
    return attribute_Dict, attribute_List, class_count, marker
    
def additionalFeat(attribute_Dict, attribute_List, group_list_i, marker,row,legacy_num,i):
    attribute_Dict["ADDITIONAL FEATURES"]=str(abbrev_check(group_list_i, prof_abbrev_dict))
    add_feat=attribute_Dict["ADDITIONAL FEATURES"]
    if len(add_feat)>30:
        add_feat=add_feat[:30]  
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"ADDITIONAL_FEATURES", "Characteristic Description":add_feat})
    marker=i
    return attribute_Dict, attribute_List, marker
    
def seedBrand(attribute_Dict, attribute_List,row,legacy_num):
    brand=row["Name"][42:50].strip()
    if brand!="":
        attribute_Dict["BRAND"]=str(abbrev_check(brand, prof_abbrev_dict))
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"BRAND", "Characteristic Description":attribute_Dict["BRAND"]})
    return attribute_Dict, attribute_List
     
def seedPackageSize(attribute_Dict,attribute_List,row,legacy_num):
    seed_package_configuration=row["Name"][33:41].strip()
    if seed_package_configuration!="":
        attribute_Dict["SEED PACKAGE CONFIGURATION"]=str(abbrev_check(seed_package_configuration, prof_abbrev_dict))
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"SEED_PACKAGE_CONFIGURATION", "Characteristic Description":attribute_Dict["SEED PACKAGE CONFIGURATION"]})
    return attribute_Dict, attribute_List

def fertProduct(attribute_Dict, attribute_List, row, legacy_num, product, sap_class):
    attribute_Dict["PRODUCT"]=product
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PRODUCT", "Characteristic Description":attribute_Dict["PRODUCT"], "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def fertPercent(attribute_Dict, attribute_List, row, legacy_num, percent, sap_class):
    attribute_Dict["PERCENTAGE CONCENTRATION"]=percent
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PERCENTAGE_CONCENTRATION", "Characteristic Description":attribute_Dict["PERCENTAGE CONCENTRATION"], "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
def fertForm(attribute_Dict, attribute_List, row, legacy_num, sap_class):
    form="DRY"
    if sap_class=="M_FERT_MICRO_LIQ":
        form="LIQUID"
                
    attribute_Dict["MICRO NUTRIENT FORM"]=form
    attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"MICRO_FORM", "Characteristic Description":attribute_Dict["MICRO NUTRIENT FORM"], "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def fertAddFact(attribute_Dict, attribute_List, row, legacy_num, sap_class, add_fact):
    if add_fact!="":
        attribute_Dict["ADDITIONAL FACTORS"]=add_fact
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"ADDITIONAL_FACTORS", "Characteristic Description":attribute_Dict["ADDITIONAL FACTORS"], "SAP Class":sap_class})
    return attribute_Dict, attribute_List
def fertPackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class):
    if row["ItemDescriptionPart2"]!="":
        attribute_Dict["PACKAGE CONFIGURATION"]=row["ItemDescriptionPart2"].strip()
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PACKAGE_CONFIGURATION", "Characteristic Description":attribute_Dict["PACKAGE CONFIGURATION"], "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def fertBrand(attribute_Dict, attribute_List, row, legacy_num, sap_class):
    if str(row["ItemDescriptionPart3"])!="nan":
        attribute_Dict["BRAND"]=str(row["ItemDescriptionPart3"]).strip()
        attribute_List.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"BRAND", "Characteristic Description":attribute_Dict["BRAND"], "SAP Class":sap_class})
    return attribute_Dict, attribute_List
