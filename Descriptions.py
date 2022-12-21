import pandas as pd
from AbbrevAndChar import abbrev_check, prof_abbrev_dict, sap_abbrev_dict

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
